import csv
import json
from pathlib import Path

from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


from lib.sitter.ast2core import ASTParse

from apps.labeling.models import PosMethodMaster, NegMethodMaster, ProjectMaster, MethodWaitMaster

from apps.labeling.models import QuesMaster

from apps.labeling.models import MethodQues


def index(request):
    user = request.user if request.user.is_authenticated else None
    context = {
        'active_menu': 'homepage',
        'user': user
    }
    return render(request, 'labeling/index.html', context)

@csrf_exempt
def create_project(request):
    data = json.loads(request.body)
    print(data)
    project_path = Path(data["path"])
    method_count = 0
    class_count = 0
    new_project = ProjectMaster(
        project_name=data['name'],
        method_count=method_count,
        class_count=class_count
    )
    new_project.save()
    try:
        ast = ASTParse(project_path, "java")
        ast.setup()
        sr_project = ast.do_parse()
        for program in sr_project.program_list:
            class_count += len(program.class_list)
            for clas in program.class_list:
                # method_count += len(clas.method_list)
                for method in clas.method_list:
                    loc = method.get_method_LOC()
                    if loc < 5:
                        continue
                    try:
                        new_method = MethodWaitMaster(
                            method_name=method.method_name,
                            class_name=clas.class_name,
                            param_count=len(method.param_list),
                            return_type=method.return_type,
                            project_id=new_project.project_id,
                            path=program.program_name,
                            content=method.to_string(space=0)
                        )
                        new_method.save()
                        method_count += 1
                    except Exception as e:
                        print(e)
                        continue
        new_project.method_count = method_count
        new_project.class_count = class_count
        new_project.save()

        return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

@csrf_exempt
def project_list(request):
    project_list = ProjectMaster.objects.all()
    re = serializers.serialize('json', project_list)

    return HttpResponse(re, content_type="text/json-comment-filtered")

@csrf_exempt
def ques_list(request):
    ques_list = QuesMaster.objects.all()
    re = serializers.serialize('json', ques_list)

    return HttpResponse(re, content_type="text/json-comment-filtered")


@csrf_exempt
def method_list(request):
    pid = request.GET['pid']
    method_list = MethodWaitMaster.objects.filter(
        project_id=pid,
        reviewed=False,
    )
    re = serializers.serialize('json', method_list)

    print(pid)
    return HttpResponse(re, content_type="text/json-comment-filtered")


@csrf_exempt
def code_table(request):
    data = json.loads(request.body)
    print(data)
    class_name = data['class_name']
    method_name = data['method_name']
    pc = data['pc']
    project_path = Path(data["path"])
    project_path = project_path

    try:
        ast = ASTParse(project_path, "java")
        ast.setup()
        sr_project = ast.do_parse_one_file(project_path)
        for program in sr_project.program_list:
            for clas in program.class_list:
                for method in clas.method_list:
                    if method.method_name == method_name \
                            and clas.class_name == class_name \
                            and str(len(method.param_list)) == str(pc):
                        method.refresh_sid()
                        stb = method.to_string_table()
                        return JsonResponse(stb, safe=False)
        return HttpResponseBadRequest()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

@csrf_exempt
def post_pos(request):
    data = json.loads(request.body)
    method_id = data["method_id"]
    method_name = data["method_name"]
    class_name = data["class_name"]
    param_count =data["param_count"]
    return_type = data["return_type"]
    project_id = data["project_id"]
    path = data["path"]
    content = data["content"]
    level = data["level"]
    ex_pos = data["ex_pos"]

    new_pos = PosMethodMaster(
        method_id=method_id,
        method_name=method_name,
        class_name=class_name,
        param_count=param_count,
        return_type=return_type,
        project_id=project_id,
        path=path,
        content=content,
        level=level,
        ex_pos=ex_pos
    )
    new_pos.save()

    method_w = MethodWaitMaster.objects.get(method_id=method_id)
    method_w.reviewed = True
    method_w.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def post_neg(request):
    data = json.loads(request.body)
    method_id = data["method_id"]
    method_name = data["method_name"]
    class_name = data["class_name"]
    param_count =data["param_count"]
    return_type = data["return_type"]
    project_id = data["project_id"]
    path = data["path"]
    content = data["content"]
    new_neg = NegMethodMaster(
        method_id=method_id,
        method_name=method_name,
        class_name=class_name,
        param_count=param_count,
        return_type=return_type,
        project_id=project_id,
        path=path,
        content=content
    )
    new_neg.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def post_ques(request):
    data = json.loads(request.body)
    ques_id = data['ques_id']
    method_id = data['method_id']
    answer = data['answer']
    new_method_ques = MethodQues(
        ques_id=ques_id,
        method_id=method_id,
        answer=answer
    )
    new_method_ques.save()
    return JsonResponse(data, safe=False)

@csrf_exempt
def export_csv(request):
    data = json.loads(request.body)
    save_path = Path(data["save_path"])
    project_id = data["project_id"]
    project_name = ProjectMaster.objects.get(project_id=project_id).project_name
    pos_method_l = PosMethodMaster.objects.filter(project_id=project_id)
    neg_method_l = PosMethodMaster.objects.filter(project_id=project_id)
    method_l = []
    method_l.extend(pos_method_l)
    method_l.extend(neg_method_l)

    node_field_order = ["id", 'path', 'class_name', 'method_name', 'param_count', 'return_type', 'ex_pos', 'level', 'project']
    with open(save_path / "index.csv", 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, node_field_order)
        writer.writeheader()
        for m in method_l:
            writer.writerow(dict(zip(node_field_order, [m.method_id, m.path,
                                                        m.class_name, m.method_name,
                                                        m.param_count, m.return_type,
                                                        m.ex_pos, m.level, project_name])))

    return JsonResponse(data, safe=False)


def review(request):
    user = request.user if request.user.is_authenticated else None
    context = {
        'active_menu': 'review',
        'user': user
    }
    return render(request, 'labeling/review.html', context)