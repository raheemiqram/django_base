from django import forms


class NLPTaskForm(forms.Form):
    prompt = forms.CharField(label='Prompt', widget=forms.Textarea)


class GMTaskForm(forms.Form):
    prompt = forms.CharField(label='Prompt', widget=forms.Textarea)
    model = forms.ChoiceField(
        choices=[('davinci', 'Davinci'), ('curie', 'Curie'), ('babbage', 'Babbage'), ('ada', 'Ada')], label='Model',
        widget=forms.Select)
    temperature = forms.FloatField(label='Temperature', initial=0.5, min_value=0.1, max_value=1.0,
                                   widget=forms.NumberInput(attrs={'step': '0.1'}))


class CVTaskForm(forms.Form):
    image = forms.ImageField(label='Image')
    model = forms.ChoiceField(
        choices=[('image-classification', 'Image Classification'), ('object-detection', 'Object Detection')],
        label='Model', widget=forms.Select)


class NLTKTrainForm(forms.Form):
    train_data = forms.CharField(widget=forms.Textarea)


class NLTKChatForm(forms.Form):
    message = forms.CharField()
