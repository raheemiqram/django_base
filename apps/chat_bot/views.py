import nltk
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
import openai
from nltk import UnigramTagger
from nltk.chat import Chat
from nltk.chat.iesha import reflections

from apps.chat_bot.forms import NLPTaskForm, GMTaskForm, CVTaskForm, NLTKTrainForm, NLTKChatForm


class NLPTaskView(FormView):
    template_name = 'dashboard/bot/nlp.html'
    form_class = NLPTaskForm
    success_url = reverse_lazy('nlp')

    def form_valid(self, form):
        prompt = form.cleaned_data['prompt']
        openai.api_key = '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'
        response = openai.Completion.create(
            engine='davinci',
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        self.request.session['prompt'] = prompt
        self.request.session['response'] = response.choices[0].text.strip()

        return super().form_valid(form)


class GMTaskView(FormView):
    template_name = 'dashboard/bot/gm.html'
    form_class = GMTaskForm
    success_url = reverse_lazy('gm')

    def form_valid(self, form):
        prompt = form.cleaned_data['prompt']
        model = form.cleaned_data['model']
        temperature = form.cleaned_data['temperature']

        openai.api_key = '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'
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=temperature,
        )

        self.request.session['prompt'] = prompt
        self.request.session['response'] = response.choices[0].text.strip()

        return super().form_valid(form)


class CVTaskView(FormView):
    template_name = 'dashboard/bot/cv.html'
    form_class = CVTaskForm
    success_url = reverse_lazy('cv')

    def form_valid(self, form):
        image = form.cleaned_data['image']
        model = form.cleaned_data['model']

        openai.api_key = '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'
        result = None
        if model == 'image-classification':
            response = openai.Image.create(
                prompt='classify the image',
                image=image,
                n=1,
            )
            result = response.output[0].text.strip()
        elif model == 'object-detection':
            response = openai.Image.create(
                prompt='detect the objects in the image',
                image=image,
                n=1,
            )
            result = ', '.join([obj.name for obj in response.output[0].objects])

        self.request.session['image'] = image.name
        self.request.session['model'] = model
        self.request.session['result'] = result

        return super().form_valid(form)


class NLTKTrainView(FormView):
    template_name = 'dashboard/nltk/train.html'
    form_class = NLTKTrainForm

    def form_valid(self, form):
        # Load the training data from the form
        train_data = form.cleaned_data['train_data']

        # Tokenize the training data and split it into a training set and a test set
        data = nltk.sent_tokenize(train_data)
        train_data = data[:int(len(data) * 0.8)]
        test_data = data[int(len(data) * 0.8):]

        # Train the tagger on the training set
        tagger = UnigramTagger(train_data)

        # Evaluate the tagger on the test set
        accuracy = tagger.evaluate(test_data)
        print("Accuracy:", accuracy)

        # Return a response indicating that the training was successful
        return JsonResponse({'status': 'success', 'accuracy': accuracy})


class NLTKChatView(FormView):
    template_name = 'dashboard/nltk/chat.html'
    form_class = NLTKChatForm

    def form_valid(self, form):
        # Get the user's message from the form
        message = form.cleaned_data['message']

        # Create the chatbot using the trained model
        pairs = [
            (r'hi|hello|hey', ['Hello!', 'Hi there!']),
            (r'what is your name?', ['My name is Abdur Raheem.']),
            (r'how are you?', ['I am doing well, thank you.', 'I am doing great!']),
            (r'bye|goodbye', ['Goodbye!', 'See you later.']),
        ]
        chatbot = Chat(pairs, reflections)

        # Generate a response from the chatbot
        response = chatbot.respond(message)

        # Render the chat template with the response
        return render(self.request, self.template_name, {'form': form, 'response': response})
