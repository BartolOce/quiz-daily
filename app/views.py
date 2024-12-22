from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.utils.timezone import now, timedelta
from .models import Question, MultipleChoiceQuestion, YesNoQuestion, QuestionAttempt, UserProfile
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import login

# Create your views here.
def index(request):
    # Default to English if no language is set
    language = request.session.get('language', 'eng')

    nav_links = {
        'cro': {'quiz': 'quiz-cro'},
        'eng': {'quiz': 'quiz-eng'},
        'ger': {'quiz': 'quiz-ger'},
    }
    content = {
        'cro': {'subtitle': 'Pratite nas svakodnevno za naše nove izazove.', 'login': 'Prijava', 'guest': 'Igraj kao gost', 'play': 'Započni igru'},
        'eng': {'subtitle': 'Tune in daily, for our new challenges.', 'login': 'Log in', 'guest': 'Play as guest', 'play': 'Start the Game'},
        'ger': {'subtitle': 'Täglich einschalten für neue Herausforderungen.', 'login': 'Anmelden', 'guest': 'Als Gast spielen', 'play': 'Wiedergabe starten'},
    }
    context = {
        'date': datetime.now().date(),
    }
    return render(request, 'app/index.html', {
        'context': context,
        'nav_links': nav_links[language],
        'content': content[language],
    })

def change_language(request, lang):
    if request.method == "POST":  # Ensure only POST requests are accepted
        request.session['language'] = lang
    return redirect('index')  # Redirect to the home page (or any page)

def quiz(request, lang):
    today = datetime.now().date()

    # Fetch the first available question for the given language and date
    question = None
    question_subclass = None
    correct_answer = None

    # Check if there's a MultipleChoiceQuestion first
    multiple_choice_question = MultipleChoiceQuestion.objects.filter(
        question__created_at__date=today,
        question__lang=lang,
    ).first()

    if multiple_choice_question:
        question = multiple_choice_question.question
        question_subclass = multiple_choice_question
        correct_answer = multiple_choice_question.correct_option
    else:
        # If no MultipleChoiceQuestion, check for YesNoQuestion
        yes_no_question = YesNoQuestion.objects.filter(
            question__created_at__date=today,
            question__lang=lang,
        ).first()

        if yes_no_question:
            question = yes_no_question.question
            question_subclass = yes_no_question
            correct_answer = yes_no_question.correct_option

    # Variables to track if the question is already solved
    already_solved = False
    is_correct = None
    selected_option = None

    if request.user.is_authenticated:
        # Check if the question is already solved by the user
        attempt = QuestionAttempt.objects.filter(
            user=request.user,
            question=question,
        ).first()

        if attempt:
            already_solved = True
            is_correct = attempt.is_correct
            selected_option = attempt.selected_option

    else:
        # Check session for anonymous users
        last_attempts = request.session.get("last_attempts", {})
        last_attempt = last_attempts.get(lang)

        if last_attempt and last_attempt.get("date") == str(today):
            already_solved = True
            is_correct = last_attempt.get("is_correct")
            selected_option = last_attempt.get("selected_option")

    # Handle form submission
    if request.method == "POST" and not already_solved:
        question_id = request.POST.get("question_id")

        if not question_id:
            return render(request, "app/error.html", {"message": "Question ID is missing."})

        if str(question.id) != question_id:
            return render(request, "app/error.html", {"message": "Invalid question ID."})

        selected_option = request.POST.get("selected_option")

        # Check if the selected option is correct
        is_correct = selected_option == correct_answer

        if request.user.is_authenticated:
            QuestionAttempt.objects.create(
                user=request.user,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct,
            )
        else:
            # Save attempt to session for anonymous users
            last_attempts = request.session.get("last_attempts", {})
            last_attempts[lang] = {
                "date": str(today),
                "question_text": question.text,
                "correct_answer": correct_answer,
                "selected_option": selected_option,
                "is_correct": is_correct,
            }
            request.session["last_attempts"] = last_attempts
            request.session.modified = True

        already_solved = True

    # Calculate time until the next question
    next_day = (now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    context = {
        "question": question,
        "question_subclass": question_subclass,
        "already_solved": already_solved,
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "selected_option": selected_option,
        "next_day": next_day.isoformat(),
        "date": today,
        "lang": lang,
    }

    return render(request, "app/quiz.html", context)

def RegisterView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save user and profile creation
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Optional, since `form.save()` handles this
            user.save()

            # Create a user profile if necessary
            UserProfile.objects.create(user=user)

            # Log in the user and redirect
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect(reverse('index'))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'app/registration/register.html', {'form': form})




