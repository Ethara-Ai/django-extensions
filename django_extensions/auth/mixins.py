from django.contrib.auth.mixins import UserPassesTestMixin


class ModelUserFieldPermissionMixin(UserPassesTestMixin):
    model_permission_user_field = "user"

    def get_model_permission_user_field(self):
        pass

    def test_func(self):
        pass
