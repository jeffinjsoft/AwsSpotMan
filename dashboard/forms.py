from django import forms


class StackForm(forms.Form):
    # CHOICES = get_stack_choices()
    name = forms.CharField(max_length=30)
    region = forms.CharField()
    vpc = forms.CharField()
    keypair = forms.CharField()
    sg_group = forms.CharField()
    ami = forms.CharField()
    instancetype = forms.CharField()
    instanceprofile = forms.CharField()
    spotprice = forms.CharField()
    userdata = forms.CharField(required=False)
    publicip = forms.CharField()
    eip = forms.CharField(required=False)
    volume = forms.CharField(required=False)
