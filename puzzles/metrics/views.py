from django.shortcuts import render
from metrics.utils import user_metrics,calculations


def metrics_view(request):
    if request.user:
        user = request.user
        df = user_metrics()
        time_av = calculations(df,user)
    else:
        time_av = None

   
 
    return render(request,"metrics.html" ,{"time_av":time_av.to_dict(orient="records")})

# Create your views here.
