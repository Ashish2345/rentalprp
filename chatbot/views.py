from django.shortcuts import render
from django.http import JsonResponse

def chat_page(request):
    return render(request, 'chatbot/chat.html')

def get_response(request):
    user_message = request.GET.get('message', '').lower()

    if 'rent' in user_message:
        bot_message = "Rental prices in Nepal depend on the location. Popular areas like Kathmandu, Pokhara, and Lalitpur usually have higher rates."
    elif 'buy' in user_message or 'purchase' in user_message:
        bot_message = "Buying property in Nepal usually requires Nepalese citizenship. Foreign nationals generally cannot buy land or houses without special permission."
    elif 'lease' in user_message or 'agreement' in user_message:
        bot_message = "In Nepal, lease agreements are commonly made for one year with options for renewal. Always ensure a written agreement is signed."
    elif 'tenant' in user_message or 'right' in user_message:
        bot_message = "Tenants in Nepal have rights under the Rental Act, including proper notice before eviction and protection from sudden rent hikes."
    elif 'property tax' in user_message:
        bot_message = "Property tax in Nepal varies depending on the municipality and property size. It is usually paid annually."
    else:
        bot_message = "I'm here to help with property rentals, purchases, leases, and tenant rights in Nepal! Please ask me anything related."

    return JsonResponse({'reply': bot_message})
