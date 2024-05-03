from django import template
from application.models import Classes, CompetitiveExam, HomePageCounts, Papers, PopupContent, Subjects, CompetitiveExam, OlympiadExam
from django.urls import reverse


register = template.Library()


@register.simple_tag
def get_five_class_exams():
     class_exams = Classes.objects.all().order_by("-purchase_count")[:5]
     return class_exams

@register.simple_tag
def get_five_competitive_exams():
     competitive_exams = CompetitiveExam.objects.all().order_by("-purchase_count")[:5]
     return competitive_exams

@register.simple_tag
def space_replace(value):
      return str(value).replace(" ","%20")

@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag
def get_home_counts():
     home_counts = {}
     if HomePageCounts.objects.all().exists():
          home_counts = HomePageCounts.objects.all().first()
     else:
          home_counts = HomePageCounts.objects.create()
     return home_counts

@register.simple_tag
def get_popup_exams():
     # image = "https://i.ibb.co/VmfmdJF/33d6de20-5fa0-4fdf-a661-eaeaab8d9a43.jpg"
     # last_paper = False
     # last_paper_url = ""
     # show_discount = False
     # discount = 0
     # if Papers.objects.all().exists():
     #      last_paper = Papers.objects.all().order_by("-id").last()
     #      discount = int(((last_paper.price - last_paper.repay_price)/last_paper.price)*100)
     #      last_paper_url = reverse("application:school_paper_wise")
     #      if Subjects.objects.filter(assigned_papers = last_paper).exists():
     #           show_discount = True
     #           last_paper_subject = Subjects.objects.filter(assigned_papers = last_paper).first()
     #           if Classes.objects.filter(assigned_subjects = last_paper_subject).exists():
     #                last_paper_class = Classes.objects.filter(assigned_subjects = last_paper_subject).first()
     #                last_paper_url = f"{last_paper_url}?class={last_paper_class.id}"
     #      elif CompetitiveExam.objects.filter(assigned_papers = last_paper).exists():
     #           show_discount = True
     #           last_paper_comp = CompetitiveExam.objects.filter(assigned_papers = last_paper).first()
     #           last_paper_url = f"{last_paper_url}?competitive={last_paper_comp.id}"
     #      elif OlympiadExam.objects.filter(paper = last_paper).exists():
     #           last_paper_olymp = OlympiadExam.objects.filter(assigned_papers = last_paper).first()
     #           last_paper_url = f"{last_paper_url}?olympiad={last_paper_olymp.id}"
     if PopupContent.objects.all().exists():
          popup = PopupContent.objects.all().last()
     else:
          popup = False

     print(popup.title)

     return {"popup": popup}
