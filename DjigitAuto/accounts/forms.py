from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class DjigitAutoCreationUserForm(auth_forms.UserCreationForm):
    user = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)
