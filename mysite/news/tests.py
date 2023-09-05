from django.test import TestCase

# Create your tests here.
def news_feedback(request):

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        fakeortrue = data.get('fakeortrue')
        text = data.get('text')
        link = data.get('link')
        # print(name,text , fakeortrue ,link)

        if name == '' or fakeortrue == '':
            context['status'] = 'alert'
            return render(request, 'news/feedback.html',context)
        
        test = Feedbacks()
        test.name = name
        test.fakeortrue = fakeortrue
        test.text = text
        test.link = link
        test.save()
        context['status'] = ['success']

        
    return render(request, 'news/feedback.html',context)