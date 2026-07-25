from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'super_admin'


class RoleFilterMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.role == 'super_admin':
            return qs
        if user.role == 'professor':
            return self._filter_professor(qs, user)
        if user.role == 'aluno':
            return self._filter_aluno(qs, user)
        return qs.none()

    def _filter_professor(self, qs, user):
        try:
            filiais = user.professor_profile.filiais.all()
            if hasattr(self.model, 'filial'):
                return qs.filter(filial__in=filiais)
        except:
            pass
        return qs.none()

    def _filter_aluno(self, qs, user):
        if hasattr(self.model, 'cpf'):
            return qs.filter(cpf=user.cpf)
        return qs.none()


class ProfessorAccessMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser or self.request.user.role == 'super_admin':
            return True
        if self.request.user.role == 'professor':
            return True
        return False


class RoleFilterDetailMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or user.role == 'super_admin':
            return obj
        if user.role == 'professor':
            try:
                filiais = user.professor_profile.filiais.all()
                if hasattr(obj, 'filial') and obj.filial in filiais:
                    return obj
            except:
                pass
        if user.role == 'aluno':
            if hasattr(obj, 'cpf') and obj.cpf == user.cpf:
                return obj
        from django.http import Http404
        raise Http404

