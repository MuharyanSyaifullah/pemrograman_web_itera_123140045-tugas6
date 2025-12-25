import json
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

from ..models import Matakuliah


def _json(payload, status=200):
    return Response(
        body=json.dumps(payload),
        status=status,
        content_type="application/json",
    )


def _get_json_body(request):
    try:
        return request.json_body
    except Exception:
        raise HTTPBadRequest(json.dumps({"error": "Body harus JSON"}))


def _validate(data, partial=False):
    required = ["kode_mk", "nama_mk", "sks", "semester"]
    if not partial:
        missing = [k for k in required if k not in data]
        if missing:
            raise HTTPBadRequest(json.dumps({"error": f"Field wajib: {', '.join(missing)}"}))

    if "kode_mk" in data:
        if not str(data["kode_mk"]).strip():
            raise HTTPBadRequest(json.dumps({"error": "kode_mk tidak boleh kosong"}))

    if "nama_mk" in data:
        if not str(data["nama_mk"]).strip():
            raise HTTPBadRequest(json.dumps({"error": "nama_mk tidak boleh kosong"}))

    if "sks" in data:
        if not isinstance(data["sks"], int) or data["sks"] <= 0:
            raise HTTPBadRequest(json.dumps({"error": "sks harus integer > 0"}))

    if "semester" in data:
        if not isinstance(data["semester"], int) or data["semester"] <= 0:
            raise HTTPBadRequest(json.dumps({"error": "semester harus integer > 0"}))


@view_config(route_name="matakuliah_list")
def matakuliah_list(request):
    data = request.dbsession.query(Matakuliah).order_by(Matakuliah.id.asc()).all()
    return _json([m.to_dict() for m in data])


@view_config(route_name="matakuliah_detail")
def matakuliah_detail(request):
    mk_id = request.matchdict.get("id", "")
    if not mk_id.isdigit():
        raise HTTPBadRequest(json.dumps({"error": "id harus angka"}))

    mk = request.dbsession.get(Matakuliah, int(mk_id))
    if not mk:
        raise HTTPNotFound(json.dumps({"error": "Matakuliah tidak ditemukan"}))

    return _json(mk.to_dict())


@view_config(route_name="matakuliah_create")
def matakuliah_create(request):
    data = _get_json_body(request)
    _validate(data, partial=False)

    mk = Matakuliah(
        kode_mk=str(data["kode_mk"]).strip(),
        nama_mk=str(data["nama_mk"]).strip(),
        sks=int(data["sks"]),
        semester=int(data["semester"]),
    )

    request.dbsession.add(mk)
    request.dbsession.flush()  # supaya id terisi

    return _json(mk.to_dict(), status=201)


@view_config(route_name="matakuliah_update")
def matakuliah_update(request):
    mk_id = request.matchdict.get("id", "")
    if not mk_id.isdigit():
        raise HTTPBadRequest(json.dumps({"error": "id harus angka"}))

    mk = request.dbsession.get(Matakuliah, int(mk_id))
    if not mk:
        raise HTTPNotFound(json.dumps({"error": "Matakuliah tidak ditemukan"}))

    data = _get_json_body(request)
    _validate(data, partial=True)

    if "kode_mk" in data:
        mk.kode_mk = str(data["kode_mk"]).strip()
    if "nama_mk" in data:
        mk.nama_mk = str(data["nama_mk"]).strip()
    if "sks" in data:
        mk.sks = int(data["sks"])
    if "semester" in data:
        mk.semester = int(data["semester"])

    request.dbsession.flush()
    return _json(mk.to_dict())


@view_config(route_name="matakuliah_delete")
def matakuliah_delete(request):
    mk_id = request.matchdict.get("id", "")
    if not mk_id.isdigit():
        raise HTTPBadRequest(json.dumps({"error": "id harus angka"}))

    mk = request.dbsession.get(Matakuliah, int(mk_id))
    if not mk:
        raise HTTPNotFound(json.dumps({"error": "Matakuliah tidak ditemukan"}))

    request.dbsession.delete(mk)
    return _json({"message": "Berhasil dihapus"})
