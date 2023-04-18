from django import forms
from poll.models import Question, Choice


class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=150)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Question
        fields = ("question_text", "description")


class ChoiceForm(forms.Form):
    choice_text1 = forms.CharField(max_length=150)
    choice_text2 = forms.CharField(max_length=150)
    choice_text3 = forms.CharField(max_length=150)
    choice_text4 = forms.CharField(max_length=150)

    class Meta:
        model = Choice
        fields = "choice_text"
