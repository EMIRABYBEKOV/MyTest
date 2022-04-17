from django.shortcuts import render, redirect, get_object_or_404
from .models import Test, Question
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from .forms import CreateTestForm


User = get_user_model()


def find_screen_view(request):
    context = {}
    return render(request, "find.html", context)


def find_test_view(request, *args, **kwargs):
    context = {}

    all_tests = Test.objects.all().values('name', 'author', 'slug')

    all_test_arr = []
    for i in all_tests:
        user = User.objects.filter(pk=int(i['author']))
        dict = {
            'name': i['name'],
            'author': str(user[0]),
            'slug': i['slug']
        }
        all_test_arr.append(dict)

    context['tests'] = all_test_arr

    if request.POST:
        test_name = request.POST['test_name']
        tests = Test.objects.filter(name=f'{test_name}').values('name', 'author', 'slug')

        test_arr =[]
        for i in tests:
            user = User.objects.filter(pk=int(i['author']))
            dict = {
                'name': i['name'],
                'author': str(user[0]),
                'slug': i['slug']
            }
            test_arr.append(dict)
        context['tests'] = test_arr


    return render(request, "find.html", context)


class TestView(DetailView):

    model = Test
    context_object_name = 'test'
    template_name = 'test.html'
    slug_url_kwarg = 'slug'




def check_answers(request, *args, **kwargs):
    slug_url_kwarg = 'slug'
    test_name = request.POST.get('test_name')
    if test_name:
        test_id = Test.objects.filter(name=test_name).values('pk')
        id = [i['pk'] for i in test_id][0]
        questions = Question.objects.filter(test=id).values('question', 'answer', 'point')
        points = 0
        count_questions = 0
        true_answers = 0
        for i in questions:
            q = i['question']
            question_id = Question.objects.filter(question=q).values('pk')
            id = [i['pk'] for i in question_id][0]
            q_get = request.POST.get(f'{id}')
            answer_query = Question.objects.filter(pk=int(id)).values('answer', 'point')
            answer = [i['answer'] for i in answer_query][0]
            point = [i['point'] for i in answer_query][0]
            if q_get == answer:
                points += int(point)
                true_answers +=1
            else:
                count_questions += 1

        context = {
            'test_name': test_name,
            'all_questions': true_answers + count_questions,
            'points': points,
            'true_answers': true_answers,
        }
        print(context)
        return render(request, "result.html", context)

def create_test_view(request, *args, **kwargs):
    context = {}
    if request.POST:
        form = CreateTestForm(request.POST)
        if form.is_valid():
            # form.save()
            name = form.cleaned_data.get('name').lower()
            print(name)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = CreateTestForm()
        context['registration_form'] = form
    return render(request, 'create_test.html', context)



