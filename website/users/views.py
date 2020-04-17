from django.core import serializers
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from users import Checksum
from website.settings import EMAIL_HOST_USER
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from users.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
import re
import logging
from itertools import chain
from django.db.models import Count, Subquery, Q
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.sites.shortcuts import get_current_site

logger = logging.getLogger(__name__)
MERCHANT_KEY = 'H&i6IFlA9Lzy_hqA'

def tests(request):
  try:
    rest_id= request.GET.get('id', None)[5:]
    request.session['restaurent_id'] = int(rest_id)
    data ={
      'is_success': 'done'
    }
    return JsonResponse(data)
  except Exception as e:
    logger.error(e)
    data={
      'is_success': 'notDone'
    }
    return JsonResponse(data)

def index(request):
    return render(request, 'overview.html')


def log_in(request):
  try:
    if request.session.get('user_id'):
      return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
      form = name_users(request.POST)   
      if form.is_valid():      
        username = request.POST['username']  
        password = request.POST['password'] 
        user = authenticate(request, username = username, password=password)
        if user:
          login(request, user)
          if request.GET.get('next', None):
            return HttpResponseRedirect(request.GET['next'])
          return HttpResponseRedirect(reverse('home'))
        else:
          return render(request, 'users/login.html', {'form' : form, 'error':'please give us right password'})
    else:
        form = name_users()
        return render(request, 'users/login.html', {'form' : form})
  except Exception as e:
    logger.error(e)
    return render(request, 'users/login.html', {'form' : form})

@login_required(login_url='/users/login/')
def home(request):
  # city=request.ipinfo.city
  key = request.session.session_key
  user=request.user
  request.session['user_id']=request.user.id
  context={}
  current_site = request.session.get('user_id')
  if request.role == 'user':
    # city_name = request.ipinfo.city
    # restaurent= Restaurents.objects.filter(city=city_name).order_by('-avarage_ratings')[:4]
    restaurent= Restaurents.objects.order_by('-avarage_ratings')[:4]
    arr=[]
    for rest in restaurent:
      shipper = Shippers.objects.filter(start_duty=True, locality=rest.locality, is_in_order=False)
      if len(shipper) > 0:
        arr.append(rest)
    if len(arr) > 0:
      context['allrestaurents'] = arr
    # restaurent= Restaurents.objects.filter(city='Bengaluru').order_by('-avarage_ratings')[:4]
    logger.error('Somehing gone wrong.')
    return render(request, 'users/home.html', context)
  else:
    logout(request)
    context['error'] = 'please give us right username and password.'
    return HttpResponseRedirect(reverse('login'), context)



@login_required(login_url='/users/login/')
def home_all_restaurents(request):
  try:
    context={}
    if request.role == 'user':
      locality = Restaurents.objects.values('locality').annotate(num_res=Count('name'))
      context['locality'] = locality
      cousines = Category.objects.values('name').annotate(num_res=Count('name')).order_by('name')
      context['cousines'] = cousines
      category = Category.objects.all()
      restaurents = Restaurents.objects.all().order_by('-avarage_ratings')
      page_no = request.GET.get('page', 1)
      paginator = Paginator(restaurents, 2)
      try:
        restaurent=paginator.page(page_no)

      except PageNotAnInteger:
        restaurent=paginator.page(1)

      except EmptyPage:
        restaurent = paginator.page(paginator.num_pages)
      context['allrestaurents'] = restaurent
      context['categorys'] = category

      return render(request, 'users/allrestaurent.html', context)
  except Exception as e:
    logger.error(e)
    return render(request, 'users/allrestaurent.html', context)


@login_required(login_url='/users/login/')
def specification(request, id):
  request.session['restaurent_id'] = id
  key = request.session.get('restaurent_id')
  user = request.session.get('user_id')
  context={}
  try:
    restaurent = Restaurents.objects.get(id= id)
  except:
    raise Http404('Dose not exists this restaurent.')
  reviews = Reviews.objects.filter(restaurents_id=restaurent).order_by('-date')
  rate = Ratings.objects.filter(coustomer_id=request.user.id, restaurents_id=restaurent)
  context['rate'] = rate
  context['reviews'] = reviews
  context['rest_info'] = restaurent
  category = Category.objects.all().filter(restaurent = restaurent.id)
  context['category'] = category
  return render(request,'users/informres.html', context)


@login_required(login_url='/users/login/')
def order_now(request):
  context={}
  key = request.session.get('restaurent_id')
  restaurents= Restaurents.objects.get(id= key)
  context['rest_info'] = restaurents
  category = Category.objects.all().filter(restaurent = restaurents.id)
  foods = Foods.objects.all().filter(restaurent = restaurents.id)
  context['category'] = category
  context['foods'] = foods
  return render(request, 'users/order.html', context)

def order_details(request, id):
    if request.method =='POST':
      context={}
      user = request.user
      try:
        restaurents = Restaurents.objects.get(id = id) #restaurent
      except:
        raise Http404('restaurents does not exist')
      context['rest_info'] = restaurents
      qty = request.POST['orderqty']
      qty = qty.split(',')
      total_prices = 0
      items = request.POST['ordritems']
      spliting = items.split(',')
      i=0
      food_details = []
      while i < len(spliting):
        final_qty = re.findall(r'\d+', qty[i])
        final_qty = int(final_qty[0])#1/2
        temp = re.findall(r'\d+', spliting[i]) #41=
        food_id = Foods.objects.get(id = int(temp[0])) #food info
        obj = {
          'food':food_id,
          'qty' : final_qty
        }
        food_details.append(obj)
        total_prices += final_qty * float( food_id.price )
        i += 1
      if total_prices !=0:
        context['food_details'] = food_details
        context['total_price'] = total_prices
        return render(request, 'users/orderConf.html', context)
    else:
      return HttpResponseRedirect(reverse('order'))

@login_required(login_url='/users/login/')
def cuisine(request, name):
  context={}
  if request.role == 'user':
    category = Category.objects.filter(name = name)
    page_no = request.GET.get('page', 1)
    restaurents= Restaurents.objects.filter(category__name__istartswith=name)
    paginator =Paginator(restaurents, 2)
    try:
      restaurent = paginator.page(page_no)

    except PageNotAnInteger:
      restaurent = paginator.page(1)

    except EmptyPage:
      restaurent = paginator.page(paginator.num_pages)

    locality = Restaurents.objects.values('locality').annotate(num_res=Count('name'))
    context['locality'] = locality
    cousines = Category.objects.values('name').annotate(num_res=Count('name')).order_by('name')
    context['cousines'] = cousines
    if len(restaurent) >0:
      context['allrestaurents'] = restaurent
      context['categorys'] = category
      return render(request, 'users/allrestaurent.html', context)
    else:
      context['allrestaurents'] = '0'
      context['categorys'] = category
      context['no_result'] = 'There has no  restaurent.'
      return render(request, 'users/allrestaurent.html', context)  

@login_required(login_url='/users/login/')
def locality(request, locality):
  context={}
  if request.role == 'user':
    category = Category.objects.all()
    restaurents= Restaurents.objects.filter(locality__istartswith=locality)
    page_no = request.GET.get('page', 1)
    paginator = Paginator(restaurents, 2)
    try :
      restaurent = paginator.page(page_no)
    except PageNotAnInteger:
      restaurent = paginator.page(1)
    except EmptyPage:
      restaurent = paginator.page(paginator.num_pages)
    localitys = Restaurents.objects.values('locality').annotate(num_res=Count('name'))
    context['locality'] = localitys
    cousines = Category.objects.values('name').annotate(num_res=Count('name')).order_by('name')
    context['cousines'] = cousines
    if len(restaurents) >0:
      context['allrestaurents'] = restaurent
      context['categorys'] = category
      return render(request, 'users/allrestaurent.html', context)
    else:
      context['allrestaurents'] = '0'
      context['categorys'] = category
      context['no_result'] = 'There has no  restaurent.'
      return render(request, 'users/allrestaurent.html', context)  

def ratings(request, id, rate):
  user = request.user
  rest_id = id
  rates = rate
  restaurent = Restaurents.objects.get(pk=rest_id)
  obj, create = Ratings.objects.get_or_create(coustomer_id=user, restaurents_id=restaurent)
  if create:
    obj.rate = rates
    obj.save()
    total_ratings = Ratings.objects.filter(restaurents_id=rest_id)

    avarage_ratings = restaurent.avarage_ratings
    total_rating = avarage_ratings * (len(total_ratings)-1)
    avg = total_rating + int(rates)
    restaurent.avarage_ratings = avg/ len(total_ratings)
    restaurent.save()
  else:
    previous_rate = obj.rate
    obj.rate = rates
    obj.save()
    total_ratings = Ratings.objects.filter(restaurents_id= rest_id)
    avarage_ratings = restaurent.avarage_ratings
    total_rating = avarage_ratings * (len(total_ratings))
    avg = (total_rating-previous_rate) + int(rates)
    restaurent.avarage_ratings = avg /len(total_ratings)
    restaurent.save()
  return HttpResponseRedirect(reverse('specification_of_restaurent', kwargs={'id':rest_id}))


def reviews(request, id):
    if request.method == 'POST':
        texts= request.POST['text']
        user= request.user
        restaurent = Restaurents.objects.get(pk = id)

        instance_reviews = Reviews.objects.create(coustomer_id = user, restaurents_id = restaurent, comment = texts)
        instance_reviews.save()
        restaurent.total_reviews = restaurent.total_reviews + 1
        restaurent.save()
        return HttpResponseRedirect(reverse('specification_of_restaurent',  kwargs={'id':id}))




def signup(request):
    if request.method == 'POST':
        form = new_user(request.POST)
        if form.is_valid():
          user_name = form.cleaned_data['username']
          f_name = form.cleaned_data['f_name']
          l_name = form.cleaned_data['l_name']
          email = form.cleaned_data['email']
          password = form.cleaned_data['password']
          conf_password = form.cleaned_data['conf_password']
          if password == conf_password:
            user = User.objects.create_user(username=user_name, first_name=f_name, last_name = l_name, email=email, password=password)
            user.save()
            user_designation = user_designations(user = user, designations='user')
            user_designation.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
          
    else:
        form = new_user()
        return  render(request, 'signup.html', {'form': form})



@login_required(login_url = '/users/login/')
def log_out(request):
  if(request.role == 'delivery'):
    ids = request.user.id
    order = Orders.objects.filter(
      Q(order_statuses='RD', shipper_id=ids) | Q(order_statuses='P&D', shipper_id=ids) | Q(order_statuses='A&P', shipper_id=ids)
    )
    if len(order) == 0:
      Shippers.objects.filter(shipper=ids).update(start_duty=False)
      logout(request)
  else:
    logout(request)
  return HttpResponseRedirect(reverse('overview'))


@login_required(login_url = '/users/login/')
def order_history(request):
  context = {}
  order_ids = Orders.successfull_order.filter( user_id = request.user).order_by('-order_date')
  orders_details =[]
  for i in order_ids:
    orders = Orderdetails.objects.filter( order_id = i)
    orders_details.append(orders)
  context['orders'] = order_ids
  context['order_details'] = orders_details
  return render(request, 'users/orderhistory.html', context)



def searching(request):
  context={}
  if request.method == 'GET':
    location = request.GET.get('location','')
    food = request.GET.get('foodOrRestaurent', '')
    if location =='' and food!='':
      foods = Restaurents.objects.filter(foods__foods_name__icontains = food)
      # foods = foods.filter(city= request.ipinfo.city)
      foods = foods.filter(city= 'Bengaluru')
      localitys = Restaurents.objects.values('locality').annotate(num_res=Count('name'))
      context['locality'] = localitys
      cousines = Category.objects.values('name').annotate(num_res=Count('name')).order_by('name')
      context['cousines'] = cousines
      context['allrestaurents'] = foods
      context['cuisines'] = Category.objects.all()
      return render(request, 'users/allrestaurent.html', context)

    elif location !='' and food == '':
      # allrest = Restaurents.objects.filter(city = request.ipinfo.city)
      allrest = Restaurents.objects.filter(city = 'Bengaluru')
      rest = allrest.filter(locality = location).exists()
      if rest:
        context['allrestaurents'] = allrest.filter(locality = location)
      else:
        context['allrestaurents'] = allrest
      localitys = Restaurents.objects.values('locality').annotate(num_res=Count('name'))
      context['locality'] = localitys
      cousines = Category.objects.values('name').annotate(num_res=Count('name')).order_by('name')
      context['cousines'] = cousines
      context['cuisines'] = Category.objects.all()
      return render(request, 'users/allrestaurent.html', context)

    else:
      localitys = Restaurents.objects.values('locality').annotate(num_res=Count('name'))
      context['locality'] = localitys
      cousines = Category.objects.values('name').annotate(num_res=Count('name')).order_by('name')
      context['cousines'] = cousines
      context['cuisines'] = Category.objects.all()
      allrest = Restaurents.objects.filter(city = request.ipinfo.city)
      rest = allrest.filter(locality = location).exists()
      if rest:
        foods = Restaurents.objects.filter(foods__foods_name__icontains=food)
        # foods = foods.filter(city=request.ipinfo.city)
        foods = foods.filter(city='Bengaluru')
        foods = foods.filter(locality=location)
        context['allrestaurents'] =foods
      else:
        foods = Restaurents.objects.filter(foods__foods_name__icontains=food)
        # foods = foods.filter(city=request.ipinfo.city)
        foods = foods.filter(city='Bengaluru')
        context['allrestaurents'] = foods
      return  render(request, 'users/allrestaurent.html', context)



def answer_me(request):
  # user_city = request.ipinfo.city
  user_city = 'Bengaluru'
  location = request.GET.get('text')
  allrestaurents_in_this_location = Restaurents.objects.filter(city = user_city)
  allrestaurents_in_this_location = allrestaurents_in_this_location.filter(locality__icontains=location).values('locality').distinct()
  if allrestaurents_in_this_location:
    # data = serializers.serialize('json', allrestaurents_in_this_location) #postgrace..
    data = list(allrestaurents_in_this_location)
    # return HttpResponse(data, content_type="application/json")  ##postgrace
    return JsonResponse(data, safe=False)
  else:
    data = []

    return JsonResponse(data, safe=False)

def cousin_or_restaurent(request):
  text = request.GET.get('text')
  cousin = Foods.objects.filter(foods_name__icontains=text).values('foods_name').distinct()
  # cousin = cousin.distinct('locality')
  # desc = Foods.objects.filter(description__icontains=text).distinct('description') ##postgrace
  categorys = Category.objects.filter(name__icontains=text).values('name').distinct()
  # restaurent_city=request.ipinfo.city
  restaurent_city='Bengaluru'
  resturent = Restaurents.objects.filter(city=restaurent_city)
  restaurent = resturent.filter(name__icontains = text).values('name').distinct()
  # data=  list(chain(cousin, categorys, resturent))
  # data =list(cousin)
  # data = serializers.serialize('json', data) ##postgrace
  # return HttpResponse(data, content_type="application/json")  ##postgrace
  cousin = list(cousin)
  category = list(categorys)
  restaurent = list(restaurent)
  data = {
    'foods': cousin,
    'category': category,
    'restaurent': restaurent
  }
  return JsonResponse(data, safe=False)

def search_and_redirect(request):
  text = request.GET.get('text')
  type = request.GET.get('type')
  id = int(request.GET.get('data-attr',0))
  if id !=0:
      return HttpResponseRedirect(reverse('specification_of_restaurent', kwargs={'id':id}))
  else:
    context = {}
    category = Category.objects.filter(name=text)

    if type=='cousin':
      restaurents = Restaurents.objects.filter(category__name__icontains=text)
    elif type == 'food':
      restaurents = Restaurents.objects.filter(foods__foods_name__icontains=text).distinct()

    locality = Restaurents.objects.values('locality').annotate(num_res=Count('name'))
    context['locality'] = locality
    cousines = Category.objects.values('name').annotate(num_res=Count('name')).order_by('name')
    context['cousines'] = cousines
    if len(restaurents) > 0:
      page_no=request.GET.get('page', 1)
      paginator = Paginator(restaurents, 2)
      try:
        restaurent = paginator.page(page_no)

      except PageNotAnInteger:
        restaurent = paginator.page(1)

      except EmptyPage:
        restaurent = paginator.page(paginator.num_pages)

      context['allrestaurents'] = restaurent
      context['categorys'] = category
      return render(request, 'users/allrestaurent.html', context)

    else:
      context['allrestaurents'] = '0'
      context['categorys'] = category
      context['no_result'] = 'There has no  restaurent.'
      return render(request, 'users/allrestaurent.html', context)

@csrf_exempt
def handelrequest(request):
  form = request.POST
  response_dict ={}
  for i in  form.keys():
    response_dict[i] = form[i]
    if i == 'CHECKSUMHASH':
      checksum = form[i]

  verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
  if verify:
    if response_dict['RESPCODE'] =='01':
      get_order_id = response_dict['ORDERID']
      Orders.objects.filter(pk = get_order_id).update(stautus=True, order_statuses='O')
      order = Orders.objects.get(pk=get_order_id)
      subject = "Your Last Minute Labor  order no. "+ str(order.id) + " has been send to " + str(order.restaurents_id.name) +"."
      massage = "Hi, Thanks for using Last Minute Labor! Your order is in process."


      send_mail(
      subject,
      massage,
      EMAIL_HOST_USER,
      ['ssamiran472@gmail.com', ],
      fail_silently= False,
      )
    else:

      print("order is not successful because " + response_dict['RESPMSG'])

  return render(request, 'users/paymentstatus.html', {"response": response_dict})

# filter high to low..
def ratings_hight_to_low(request):
    context = {}
    if request.role == 'user':
      category = Category.objects.all()
      restaurents = Restaurents.objects.all().order_by('-avarage_ratings')
      paginator = Paginator(restaurents, 2)
      page = request.GET.get('page', 1)
      try:
        restaurent = paginator.page(page)
      except PageNotAnInteger:
        restaurent = paginator.page(1)
      except EmptyPage:
        restaurent = paginator.page(paginator.num_pages)
      localitys = Restaurents.objects.values('locality').annotate(num_res=Count('name'))
      context['locality'] = localitys
      cousines = Category.objects.values('name').annotate(num_res=Count('name')).order_by('name')
      context['cousines'] = cousines
      if len(restaurents) > 0:
        context['allrestaurents'] = restaurent

        context['categorys'] = category
        return render(request, 'users/allrestaurent.html', context)
      else:
        context['allrestaurents'] = '0'
        context['categorys'] = category
        context['no_result'] = 'There has no  restaurent.'
        return render(request, 'users/allrestaurent.html', context)


def accept_payment(request, id):
  if request.method == "POST":
    data = request.POST['hidden']
    data = data.split(',')
    email = str(User.objects.get(pk = request.user.id).id)
    x= 0
    restaurents = Restaurents.objects.get(id = id)
    order_dates = datetime.date.today()
    create_order = Orders.objects.create(user_id=request.user, restaurents_id=restaurents, order_date=order_dates)
    create_order.save()
    total_prices = 0
    while x < len(data):
      num = data[x].split('/')

      qty = re.findall(r'\d+', num[0])

      food_id = re.findall(r'\d+', num[1])
      food = Foods.objects.get(id = int(food_id[0]))

      create_order_details = Orderdetails.objects.create(order_id=create_order, food_id=food, quentity=int(qty[0]))
      create_order_details.save()
      total_prices += create_order_details.total_cost
      x += 1
    Orders.objects.filter(id= create_order.id).update(total_price=total_prices)
    param_dict = {
      'MID': 'gHpAkH96038813858302',
      'ORDER_ID': str(create_order.id),
      'TXN_AMOUNT': str(total_prices),
      'CUST_ID': email,
      'INDUSTRY_TYPE_ID': 'Retail',
      'WEBSITE': 'WEBSTAGING',
      'CHANNEL_ID': 'WEB',
      'CALLBACK_URL': 'http://127.0.0.1:8000/users/handlerequest/',

    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'users/paytm.html', {'param_dict': param_dict})

  else:
    return HttpResponse('wrong')



def payment(request):
  pass








      # delivery partner..
def delivery_partner(request):
  context ={}
  if request.method == 'POST':
    form = deliveryPartner(request.POST)
    if form.is_valid:
      users_name = request.POST['name']
      users_password = request.POST['password']
      users_mob_no = request.POST['mob_no']
      users_email = request.POST['email']
      users_identy_proof = request.POST['identy_proof']
      users_photo = request.POST['photo']
      users_driving_licence = request.POST['driving_licence']
      vachile_type= request.POST['vachile_type']
      vachile_no = request.POST['vachile_no']
      locality = request.POST['locality']
      user1 = User.objects.create_user(username=users_email, first_name=users_name,password=users_password, email=users_email)
      user1.save()
      delivery_user = Shippers(
        shipper=user1, name=users_name, mob_no=users_mob_no , identy_proof= users_identy_proof, photo= users_photo, deriving_licence= users_driving_licence, Vechile_no=vachile_no, Vachile_type=vachile_type, locality=locality
      )
      delivery_user.save()
      user_designation = user_designations(user = user1, designations = 'delivery')
      user_designation.save()
      login(request, user1)
      return HttpResponseRedirect(reverse('delivery_home'))
       
  else:
    context['form'] = deliveryPartner()
    return render(request, 'delivery/delivery.html', context)


def restaurents(request):
  context ={}
  if request.method == 'POST':
    form = resturent(request.POST, request.FILES)
    if form.is_valid():
      users_name = request.POST['email']
      users_password = request.POST['password']
      # email and password is stroed in User table
      # email is stored as username and email field
      user1 = User.objects.create_user(username=users_name, first_name=users_name,password=users_password, email=users_name)
      # save to store in db
      user1.save()
      # store all information except user information 
      # or without  liknking with  User table.
      new_restaurent_details = form.save(commit=False)
      # now store user information and save it
      new_restaurent_details.user = user1
      new_restaurent_details.save()    
      # now time to store user's designation to 
      # user_designation table.
      user_designation = user_designations(user = user1, designations = 'restaurent') 
      user_designation.save()
      # loging in the  restaurent user 
      login(request, user1)
      return HttpResponseRedirect(reverse('restaurent_home'))
    else:
      return HttpResponse('wrong')
  
  else:
    context['form2'] = resturent()
    return render(request, 'resturent/restlogin.html', context)  




def delivery_login(request):
  if request.method == 'POST':
    form = name_users(request.POST)   
     
    if form.is_valid():      
      username = request.POST['username']  
      password = request.POST['password'] 
      user = authenticate(request, username = username, password=password)
      if user:
        login(request, user)
        if request.GET.get('next', None):
          return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect(reverse('delivery_home'))
      else:
        return render(request, 'delivery/dlogin.html', {'form' : form, 'error':'please give us right password'})
 

  else:
      form = name_users()
      return render(request, 'users/login.html', {'form' : form})

@login_required(login_url = '/users/delivery/login')
def delivery_home(request):
  context ={}
  if request.role == 'delivery':
    id = request.user.id
    context['is_in_duty'] = Shippers.objects.get(shipper=id).start_duty
    delivery_id = Shippers.objects.get(shipper=id).id
    request.session['d_id']=delivery_id
    return render(request, 'delivery/home.html', context)
  else:
    logout(request)
    context['error'] = 'please give us right username and password.'
    return HttpResponseRedirect(reverse('delivery_login'))



def restaurents_login(request):
  if request.method == 'POST':
    form = name_users(request.POST)   
    if form.is_valid():
      username = request.POST['username']  
      password = request.POST['password'] 
      user = authenticate(request, username = username, password=password)
      if user:
        login(request, user)
        if request.GET.get('next', None):
          return HttpResponseRedirect(request.GET['next'])
        return HttpResponseRedirect(reverse('restaurent_home'))
      
      else:
        return render(request, 'users/login.html', {'form' : form, 'error':'please give us right password'})
 

  else:
      form = name_users()
      return render(request, 'resturent/login.html', {'form' : form})
  

@login_required(login_url = '/users/restaurent/login')
def restaurents_home(request):

  users_info = request.user.id
  rest_list = Restaurents.objects.get(user = users_info)
  request.session['restaurent']=rest_list.id
  context ={}
  if request.role == 'restaurent':
    context['users'] = rest_list
    cuisines = Category.objects.filter(restaurent=rest_list.id)
    context['cuisines'] = cuisines
    orders_count=Orders.objects.filter(restaurents_id=rest_list, seen_by_rest=False)
    context['order_count']=len(orders_count)
    context['foods_form'] = foods(rest_list.id)
    return render(request, 'resturent/home.html', context)
  else:
    logout(request)
    context['error'] = 'please give us right username and password.'
    return HttpResponseRedirect(reverse('restaurent_login'))

# adding category to db
@login_required(login_url = '/users/restaurent/login')
def addCategory(request):
  if request.method == 'POST':
    cat_name = request.POST['cuisines']
    restaurent= Restaurents.objects.get(user = request.user.id)
    category = Category(restaurent=restaurent, name = cat_name)
    category.save()
    return HttpResponseRedirect(reverse('restaurent_home'))

@login_required(login_url = '/users/restaurent/login')
def addfood(request):
  if request.method == 'POST':
    rest_list = Restaurents.objects.get(user = request.user.id)

    form = foods(rest_list.id, request.POST, request.FILES)  
    
    if form.is_valid():
      product = form.save(commit = False)
      product.restaurent = rest_list
      product.save()
      return HttpResponseRedirect(reverse('restaurent_home'))

def delete_category(request, id):
  get_object = Category.objects.get(pk=id)
  get_object.delete()
  return HttpResponseRedirect(reverse('restaurent_home'))


def show_reviews(request):
  context={}
  user_id = request.user.id
  restaurent = Restaurents.objects.get(user=user_id)
  reviews=Reviews.objects.filter(restaurents_id=user_id)
  context['allreviews'] = reviews
  return render(request, 'resturent/reviews.html', context)


def all_orders(request):
  id=request.session.get('restaurent')
  all_order = Orders.objects.filter(restaurents_id=id, stautus=True)
  all_order_orderdetails = Orderdetails.objects.filter(order_id__in=Subquery(all_order.values('pk'))).order_by('-id')
  seen_orders= Orders.objects.filter(restaurents_id=id, seen_by_rest=False)
  all_order_filter = Orders.objects.values('order_statuses').annotate(Count('order_statuses'))
  for order in seen_orders:
    Orders.objects.filter(pk=order.id).update(seen_by_rest=True)
  context={}
  context['all_orders']=all_order_orderdetails
  context['filter'] = all_order_filter
  return render(request, 'resturent/orders.html', context)


def order_info(request):
  id = request.session.get('restaurent')
  context={}
  order_id= request.GET.get('id')
  all_order = Orders.objects.filter(id=order_id)
  all_order_orderdetails = Orderdetails.objects.filter(order_id__in=Subquery(all_order.values('pk')))
  context['allinfo'] = all_order_orderdetails
  return render(request,'resturent/orderdet.html', context)


def check_order(request):
  context={}
  id=request.session.get('restaurent')
  all_order = Orders.objects.filter(
    Q(order_statuses='O', restaurents_id=id) | Q(order_statuses='A&P', restaurents_id=id) | Q(order_statuses='RD', restaurents_id=id) | Q(order_statuses='P&D', restaurents_id=id)
  )
  seen_orders = Orders.objects.filter(restaurents_id=id, seen_by_rest=False)
  for order in seen_orders:
    Orders.objects.filter(pk=order.id).update(seen_by_rest=True)
  all_order_orderdetails = Orderdetails.objects.filter(order_id__in=Subquery(all_order.values('pk')))
  context['orders'] = all_order_orderdetails
  return render(request, 'resturent/get_order.html', context)



def check_new_orders(request):
  id=request.session.get('restaurent')
  all_order = Orders.objects.filter(
   Q(order_statuses='A&P', stautus=True, restaurents_id=id) | Q(order_statuses='O', stautus=True, restaurents_id=id) | Q(order_statuses='RD', stautus=True, restaurents_id=id) | Q(order_statuses='P&D',stautus=True, restaurents_id=id)
  ).order_by('-id')
  print(all_order)
  all_order_orderdetails = Orderdetails.objects.all()
  all_order_orderdetails = all_order_orderdetails.filter(order_id__in=Subquery(all_order.values('pk'))).select_related('order_id').order_by('-id')
  foods= Foods.objects.filter(id__in=Subquery(all_order_orderdetails.values('food_id')))
  users= User.objects.filter(id__in=Subquery(all_order.values('user_id'))).values_list('email', 'pk')
  data={
    'orderdetails': serializers.serialize('json', all_order_orderdetails),
    'foods': serializers.serialize('json', foods),
    'order': serializers.serialize('json', all_order),
    'user': list(users)
    
  }
  return JsonResponse(data, safe=False)


def accept_or_decline(request):
  id= request.GET.get('id')[7:]
  accept_ordec = request.GET.get('id')[:7]
  if accept_ordec == 'orderss':
    rest_id = request.session.get('restaurent')
    rest_location = Restaurents.objects.get(pk=rest_id).locality
    shippers = Shippers.objects.filter(start_duty=True, is_in_order=False, locality=rest_location).order_by('total_order', 'id')[:1]
    Orders.objects.filter(id=id).update(order_statuses='A&P', shipper_id=shippers[0].id)
  elif accept_ordec == 'decline':
    Orders.objects.filter(id=id).update(order_statuses='R')
  data={
    'ok': id
  }
  return JsonResponse(data, safe=False)


def food_prepared(request):
  id=request.GET.get('id')[7:]
  updates=Orders.objects.filter(id=id).update(order_statuses='RD')
  data = {
    'ok': id
  }
  return JsonResponse(data, safe=False)