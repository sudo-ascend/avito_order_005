from django import forms


class PriceUploadForm(forms.Form):
    file = forms.FileField(label="Excel файл")
    should_update_prices = forms.ChoiceField(
        label="Режим",
        choices=(
            ("yes", "С merge"),
            ("no", "Без merge"),
        ),
        widget=forms.RadioSelect,
        initial="yes",
    )

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        if not uploaded_file.name.lower().endswith(".xlsx"):
            raise forms.ValidationError("Нужен файл Excel формата .xlsx")
        return uploaded_file


class MergeConfirmationForm(forms.Form):
    confirm_merge = forms.ChoiceField(
        label="Подтвердить изменение данных?",
        choices=(
            ("yes", "Да, применить изменения"),
            ("no", "Нет, оставить файл без merge"),
        ),
        widget=forms.RadioSelect,
        initial="yes",
    )
