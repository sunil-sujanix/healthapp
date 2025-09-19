from flask import Blueprint,request,jsonify,send_file
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from werkzeug.security import generate_password_hash,check_password_hash
from models import User,db,Dependent,Record,Document
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os
from sqlalchemy import func

from utils.storage import save_file,get_file_path




routes=Blueprint('routes',__name__)


@routes.route('/register',methods=['POST'])
def register():
    data=request.json
    email=data['email']
    password=data['password']
    if not email or not password:
        return jsonify({'message':'Email and Password Are Required'}),400
    try:
        
        user=User(email=email,password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message':'email already registeered'}),409
    
    return jsonify({'message':'User Registered successfully',
                    'data':{"id":user.id,"email":user.email}}),201
                    

@routes.post('/login')
def login():
    data=request.json
    email=data['email']
    
    if not email or not data["password"]:
        return jsonify({"message": "Email and password are required"}), 400
    
    
    email_user=User.query.filter_by(email=email).first()
    if not email_user or not check_password_hash(email_user.password,data["password"]):
        return jsonify({'message':'invalid details'}),401
    token = create_access_token(identity=str(email_user.id))

    return jsonify({'access_token':token,
                    'message':'login successfully',
                    'data':{"name":email_user.email}}),200
    
    
@routes.get('/deps')
@jwt_required()
def get_dependents():
    uid = int(get_jwt_identity())  # cast back to int
    rows = Dependent.query.filter_by(user_id=uid).all()
    return jsonify({
        'message': 'dependents retrieved successfully',
        'data': [{'id': d.id, "name": d.name, "relationship": d.relationship} for d in rows]
    })

    
@routes.post('/deps')
@jwt_required()
def add_dep():
    uid = int(get_jwt_identity())

    data=request.json
    if not data['name']:
        return jsonify({'message':'name is required'}),400
    d=Dependent(user_id=uid,name=data['name'],relationship=data.get("relationship","self"))
    db.session.add(d)
    db.session.commit()
    return jsonify({'id':d.id}),201





@routes.get("/records")
@jwt_required()
def list_records():
    uid = int(get_jwt_identity())

    dep_id = request.args.get("dependent_id", type=int)
    q = Record.query.filter_by(user_id=uid)
    if dep_id: q = q.filter_by(dependent_id=dep_id)
    q = q.order_by(Record.taken_at.desc())
    rows = q.all()
    return [{
      "id": r.id, "dependent_id": r.dependent_id, "kind": r.kind,
      "systolic": r.systolic, "diastolic": r.diastolic,
      "sugar_mg_dl": float(r.sugar_mg_dl) if r.sugar_mg_dl is not None else None,
      "taken_at": r.taken_at.isoformat()
    } for r in rows]
    
    


@routes.get("/analytics/bp_trend")
@jwt_required()
def bp_trend():
    uid = int(get_jwt_identity())

    q = db.session.query(
        func.date_trunc('day', Record.taken_at).label('d'),
        func.avg(Record.systolic), func.avg(Record.diastolic)
    ).filter(Record.user_id==uid, Record.kind=='blood_pressure') \
     .group_by('d').order_by('d')
    return [{"date": d.strftime("%Y-%m-%d"), "sys": float(s or 0), "dia": float(di or 0)}
            for d, s, di in q.all()]


    
    


@routes.post("/records")
@jwt_required()
def create_record():
    uid = int(get_jwt_identity())


    is_multipart = (request.content_type or "").startswith("multipart/form-data")
    data = request.form if is_multipart else (request.get_json() or {})

    dep_id = data.get("dependent_id")
    if not dep_id:
        return {"msg": "dependent_id required"}, 400

    r = Record(
        user_id=uid,
        dependent_id=dep_id,
        kind=data.get("kind", "blood_pressure"),
        systolic=data.get("systolic"),
        diastolic=data.get("diastolic"),
        sugar_mg_dl=data.get("sugar_mg_dl"),
        taken_at=datetime.fromisoformat(data["taken_at"]) if data.get("taken_at") else datetime.utcnow()
    )
    db.session.add(r)
    db.session.flush()

    # handle file upload
    if is_multipart and "file" in request.files:
        f = request.files["file"]
        key, path = save_file(f, f.filename)
        doc = Document(
            user_id=uid,
            dependent_id=dep_id,
            record_id=r.id,
            filename=f.filename,
            object_key=key,
            content_type=f.mimetype,
            size_bytes=os.path.getsize(path)
        )
        db.session.add(doc)

    db.session.commit()
    return {"id": r.id}, 201





@routes.get("/documents/<int:doc_id>/download")
@jwt_required()
def download(doc_id):
    uid = int(get_jwt_identity())

    doc = Document.query.get_or_404(doc_id)
    if doc.user_id != uid:
        return {"msg": "forbidden"}, 403
    path = get_file_path(doc.object_key)
    return send_file(path, as_attachment=True, download_name=doc.filename)

 
    
  
    
    