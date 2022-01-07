from django import forms

class ContactForm(forms.Form):
    fullname = forms.CharField(label = 'Full Name',widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Your message"}))

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if not "@" in email or email[email.find("@")+1:]==".com" or not ".com" in email :
    #         raise forms.ValidationError("Invalid email")
    #     return email