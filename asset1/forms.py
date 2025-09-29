from django import forms
from .models import Asset, AssetRequest, IssueReport

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name','category','serial_number','description','location','acquired_date','purchase_price','assigned_to','status','is_active']

class AssetRequestForm(forms.ModelForm):
    class Meta:
        model = AssetRequest
        fields = ['category','asset','reason']

class IssueReportForm(forms.ModelForm):
    class Meta:
        model = IssueReport
        fields = ['asset','issue_type','description']
