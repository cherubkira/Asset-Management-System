from django import forms
from .models import Asset, AssetRequest, IssueReport,EmployeeList, Category,SubCategory


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

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeList
        fields = ['img', 'first_name', 'last_name', 'phone_number', 'email', 'department', 'position']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name", "description", "category"]

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg text-gray-900 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Your Name'}))
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg text-gray-900 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Your Email'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg text-gray-900 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Your Message',
            'rows': 4
        })
    )