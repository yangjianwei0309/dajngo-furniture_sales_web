from cyj_furniture.models import TypeInfo
def all_tag(request):
    typeinfos = TypeInfo.objects.all()
    return {"typeof":typeinfos}