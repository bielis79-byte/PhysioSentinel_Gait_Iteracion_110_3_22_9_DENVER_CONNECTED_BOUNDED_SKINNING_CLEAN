from __future__ import annotations
from pathlib import Path
import hashlib, json, zipfile, re, functools, tempfile
import numpy as np
import trimesh

CACHE_ROOT=Path("/tmp/physiosentinel_visible_human_v3220")
SOURCE_PAGE="https://digitalcommons.du.edu/visiblehuman/"
ATTRIBUTION=(
    "Visible Human Male/Female lower-extremity musculoskeletal geometry, "
    "Center for Orthopaedic Biomechanics, University of Denver, CC BY 4.0; "
    "Andreassen et al., Scientific Data 10, 34 (2023)."
)

BONES=[
    "coccyx","sacrum","pelvis","femur","patella","tibia","fibula","talus",
    "calcaneus","navicular","cuboid","cuneiform","phalanges","metatars","tarsal"
]
MUSCLES=[
    "adductor brevis","adductor longus","adductor magnus","biceps femoris long",
    "biceps femoris short","extensor digitorum longus","extensor hallucis longus",
    "flexor digitorum longus","flexor hallucis longus","gastrocnemius lateral",
    "gastrocnemius medial","gluteus maximus","gluteus medius","gluteus minimus",
    "gracilis","iliacus","inferior gemellus","obturator externus","obturator internus",
    "pectineus","peroneus longus","fibularis longus","piriformis","plantaris","popliteus",
    "psoas major","quadratus femoris","rectus femoris","sartorius","semimembranosus",
    "semitendinosus","soleus","superior gemellus","tensor fasciae latae","tibialis anterior",
    "tibialis posterior","vastus intermedius","vastus lateralis","vastus medialis"
]

def _norm(s):
    s=str(s).lower().replace("lnferior","inferior").replace("lliacus","iliacus")
    s=s.replace("lnternus","internus").replace("lntermedius","intermedius")
    s=re.sub(r"[_\-.]+"," ",s)
    s=re.sub(r"\s+"," ",s).strip()
    return s

def _side(path_text):
    t=" "+_norm(path_text)+" "
    if any(x in t for x in (" right "," rt "," r side ","_r ")):
        return "r"
    if any(x in t for x in (" left "," lt "," l side ","_l ")):
        return "l"
    # folder/file suffixes
    low=str(path_text).lower()
    if re.search(r"(^|[/\\ _-])r($|[/\\ _-])",low): return "r"
    if re.search(r"(^|[/\\ _-])l($|[/\\ _-])",low): return "l"
    return None

def _structure(path_text):
    t=_norm(Path(path_text).stem)
    # bone first
    for x in BONES:
        if x in t:
            return "bone",x
    for x in MUSCLES:
        if x in t:
            return "muscle",x
    # broad aliases
    aliases={
        "gastrocnemius":"gastrocnemius medial",
        "peroneus":"peroneus longus",
        "fibularis":"fibularis longus",
        "gluteus":"gluteus maximus",
        "vastus":"vastus lateralis",
    }
    for a,b in aliases.items():
        if a in t: return "muscle",b
    return None,None

def _region(kind,name):
    n=_norm(name)
    if kind=="bone":
        if n in ("pelvis","sacrum","coccyx"): return "pelvis"
        if n in ("femur","patella"): return "thigh"
        if n in ("tibia","fibula"): return "shank"
        return "foot"
    hip=("gluteus","iliacus","psoas","piriformis","gemellus","obturator","pectineus",
         "quadratus femoris","tensor fasciae latae")
    thigh=("adductor","biceps femoris","gracilis","rectus femoris","sartorius",
           "semimembranosus","semitendinosus","vastus")
    if any(x in n for x in hip): return "pelvis"
    if any(x in n for x in thigh): return "thigh"
    return "shank"

def prepare_visible_human_zip(data: bytes, subject="Female"):
    sha=hashlib.sha256(data).hexdigest()[:16]
    root=CACHE_ROOT/f"{subject.lower()}_{sha}"
    root.mkdir(parents=True,exist_ok=True)
    marker=root/"manifest.json"
    if marker.exists():
        return json.loads(marker.read_text(encoding="utf-8"))
    zpath=root/"source.zip"
    zpath.write_bytes(data)
    extract=root/"stl"
    extract.mkdir(exist_ok=True)
    with zipfile.ZipFile(zpath) as z:
        for n in z.namelist():
            if n.lower().endswith(".stl"):
                try: z.extract(n,extract)
                except Exception: pass
    parts=[]
    for p in extract.rglob("*.stl"):
        kind,name=_structure(str(p))
        if not kind: continue
        side=_side(str(p))
        parts.append({
            "path":str(p),"kind":kind,"name":name,"side":side,
            "region":_region(kind,name)
        })
    man={
        "ready":bool(parts),"root":str(root),"subject":subject,"sha":sha,
        "parts":parts,"bones":sum(x["kind"]=="bone" for x in parts),
        "muscles":sum(x["kind"]=="muscle" for x in parts),
        "license":"CC BY 4.0","attribution":ATTRIBUTION,
        "source_page":SOURCE_PAGE
    }
    marker.write_text(json.dumps(man,ensure_ascii=False,indent=2),encoding="utf-8")
    return man

@functools.lru_cache(maxsize=256)
def _mesh(path):
    m=trimesh.load_mesh(path,process=False)
    if isinstance(m,trimesh.Scene):
        m=trimesh.util.concatenate(tuple(g for g in m.geometry.values()))
    V=np.asarray(m.vertices,np.float32)
    F=np.asarray(m.faces,np.int32)
    return V,F

def _unit(v,fb):
    v=np.asarray(v,float); n=np.linalg.norm(v)
    return np.asarray(fb,float) if n<1e-9 else v/n

def _pca(V):
    X=np.asarray(V,float)-np.mean(V,axis=0)
    _,_,vt=np.linalg.svd(X,full_matrices=False)
    B=vt.T
    if np.linalg.det(B)<0: B[:,2]*=-1
    return B

def _target_frame(J,nm,frame,side,region):
    pel=nm.get("pelvis")
    hip=nm.get(f"femur_{side}")
    knee=nm.get(f"tibia_{side}")
    ankle=nm.get(f"talus_{side}")
    cal=nm.get(f"calcn_{side}")
    toe=nm.get(f"toes_{side}")
    other=nm.get(f"femur_{'l' if side=='r' else 'r'}")
    lr=(J[frame,hip]-J[frame,other]) if hip is not None and other is not None else np.array([1.,0.,0.])
    if region=="pelvis":
        a=J[frame,pel] if pel is not None else J[frame,hip]
        b=J[frame,hip] if hip is not None else a+np.array([0,-.2,0])
    elif region=="thigh":
        a=J[frame,hip]; b=J[frame,knee]
    elif region=="shank":
        a=J[frame,knee]; b=J[frame,ankle]
    else:
        a=J[frame,cal] if cal is not None else J[frame,ankle]
        b=J[frame,toe] if toe is not None else J[frame,ankle]+np.array([0,0,.15])
    z=_unit(b-a,[0,-1,0])
    x=np.asarray(lr,float); x=x-np.dot(x,z)*z; x=_unit(x,[1,0,0])
    y=_unit(np.cross(z,x),[0,0,1])
    x=_unit(np.cross(y,z),x)
    return np.asarray(a,float),np.stack([x,y,z],axis=1),float(np.linalg.norm(b-a))

def _donor_reference(man,side,region):
    # select key bone
    preferred={
        "pelvis":["pelvis","sacrum"],
        "thigh":["femur"],
        "shank":["tibia","fibula"],
        "foot":["calcaneus","phalanges","talus"]
    }[region]
    cand=[p for p in man["parts"] if p["kind"]=="bone" and p.get("side") in (side,None) and p["name"] in preferred]
    if not cand:
        cand=[p for p in man["parts"] if p["kind"]=="bone" and p.get("side") in (side,None)]
    if not cand: return None
    # use first preferred hit
    p=sorted(cand,key=lambda q: preferred.index(q["name"]) if q["name"] in preferred else 99)[0]
    V,_=_mesh(p["path"])
    C=np.mean(V,axis=0)
    B=_pca(V)
    # choose longest PCA axis as local Z
    spans=np.ptp((V-C)@B,axis=0)
    iz=int(np.argmax(spans))
    others=[i for i in range(3) if i!=iz]
    z=B[:,iz]; x=B[:,others[0]]; y=_unit(np.cross(z,x),B[:,others[1]])
    x=_unit(np.cross(y,z),x)
    Bb=np.stack([x,y,z],axis=1)
    L=max(float(spans[iz]),1e-6)
    # origin at proximal extreme along local z
    q=(V-C)@Bb
    origin=C+Bb[:,2]*float(np.max(q[:,2]))
    # flip z so geometry extends primarily in + local longitudinal from origin
    Bb[:,2]*=-1
    Bb[:,1]=_unit(np.cross(Bb[:,2],Bb[:,0]),Bb[:,1])
    return origin,Bb,L

def _skin_radius(skin,a,b):
    V=np.asarray(skin,float); c=.5*(a+b); L=max(np.linalg.norm(b-a),1e-6)
    d=np.linalg.norm(V-c,axis=1)
    k=min(max(50,len(V)//100),len(V))
    if k==0:return .05*L
    pts=V[np.argpartition(d,k-1)[:k]]
    return float(np.percentile(np.linalg.norm(pts-c,axis=1),65))

def build_visible_human_frame(man,joints,joint_names,skin_vertices,frame=0,
                              show_bones=True,show_muscles=True,max_faces_each=220):
    J=np.asarray(joints,np.float32); skin=np.asarray(skin_vertices,np.float32)
    nm={str(n):i for i,n in enumerate(joint_names)}
    out=[]
    refs={}
    for side in ("r","l"):
        for region in ("pelvis","thigh","shank","foot"):
            refs[(side,region)]=_donor_reference(man,side,region)
    for p in man["parts"]:
        if p["kind"]=="bone" and not show_bones: continue
        if p["kind"]=="muscle" and not show_muscles: continue
        side=p.get("side")
        if side not in ("r","l"):
            # central pelvis/sacrum shown once on right-frame convention
            side="r"
        ref=refs.get((side,p["region"]))
        if ref is None: continue
        donor_origin,donor_B,donor_L=ref
        try:
            target_origin,target_B,target_L=_target_frame(J,nm,frame,side,p["region"])
        except Exception:
            continue
        V,F=_mesh(p["path"])
        Q=(V-donor_origin)@donor_B
        scale=target_L/max(donor_L,1e-6)
        if p["kind"]=="bone":
            transverse=scale
        else:
            # preserve muscle volume better; only mild transverse adaptation to skin
            try:
                if p["region"]=="thigh":
                    a=J[frame,nm[f"femur_{side}"]]; b=J[frame,nm[f"tibia_{side}"]]
                elif p["region"]=="shank":
                    a=J[frame,nm[f"tibia_{side}"]]; b=J[frame,nm[f"talus_{side}"]]
                else:
                    a=target_origin; b=target_origin+target_B[:,2]*target_L
                skin_r=_skin_radius(skin,a,b)
                native_r=max(np.percentile(np.linalg.norm(Q[:,:2],axis=1),70),1e-6)
                transverse=float(np.clip((skin_r*.72)/native_r,scale*.65,scale*1.35))
            except Exception:
                transverse=scale
        Qs=Q*np.array([transverse,transverse,scale])[None,:]
        W=target_origin+Qs@target_B.T

        # display decimation by deterministic face sampling
        step=max(1,int(np.ceil(len(F)/float(max_faces_each))))
        Fs=np.asarray(F[::step,:3],np.int32)
        used=np.unique(Fs.reshape(-1))
        remap=np.full(len(W),-1,np.int32); remap[used]=np.arange(len(used),dtype=np.int32)
        out.append({
            "id":f"{p['kind']}:{p['name']}:{side}",
            "kind":p["kind"],"name":p["name"],"side":side,
            "V":np.asarray(W[used],np.float32),"F":remap[Fs]
        })
    return out

def atlas_counts(man):
    if not man:return {"bones":0,"muscles":0}
    return {"bones":int(man.get("bones",0)),"muscles":int(man.get("muscles",0))}



# ---------------------------------------------------------------------------
# V110.3.22.5 · MASTER ATLAS DENVER -> HAMNER/SKEL
# ---------------------------------------------------------------------------

MUSCLE_CHAIN = {
    # pelvis / hip
    "gluteus maximus":("pelvis","thigh"), "gluteus medius":("pelvis","thigh"),
    "gluteus minimus":("pelvis","thigh"), "iliacus":("pelvis","thigh"),
    "psoas major":("pelvis","thigh"), "piriformis":("pelvis","thigh"),
    "inferior gemellus":("pelvis","thigh"), "superior gemellus":("pelvis","thigh"),
    "obturator externus":("pelvis","thigh"), "obturator internus":("pelvis","thigh"),
    "pectineus":("pelvis","thigh"), "quadratus femoris":("pelvis","thigh"),
    "tensor fasciae latae":("pelvis","thigh"),
    # thigh / knee
    "adductor brevis":("pelvis","thigh"), "adductor longus":("pelvis","thigh"),
    "adductor magnus":("pelvis","thigh"), "biceps femoris long":("pelvis","shank"),
    "biceps femoris short":("thigh","shank"), "gracilis":("pelvis","shank"),
    "rectus femoris":("pelvis","shank"), "sartorius":("pelvis","shank"),
    "semimembranosus":("pelvis","shank"), "semitendinosus":("pelvis","shank"),
    "vastus intermedius":("thigh","shank"), "vastus lateralis":("thigh","shank"),
    "vastus medialis":("thigh","shank"), "popliteus":("thigh","shank"),
    # shank / ankle-foot
    "gastrocnemius lateral":("thigh","foot"), "gastrocnemius medial":("thigh","foot"),
    "soleus":("shank","foot"), "plantaris":("thigh","foot"),
    "tibialis anterior":("shank","foot"), "tibialis posterior":("shank","foot"),
    "extensor digitorum longus":("shank","foot"), "extensor hallucis longus":("shank","foot"),
    "flexor digitorum longus":("shank","foot"), "flexor hallucis longus":("shank","foot"),
    "peroneus longus":("shank","foot"), "fibularis longus":("shank","foot"),
}

def _clean_mesh_master(path):
    """Load and lightly clean STL without changing atlas coordinates."""
    m=trimesh.load_mesh(path,process=True)
    if isinstance(m,trimesh.Scene):
        m=trimesh.util.concatenate(tuple(g for g in m.geometry.values()))
    try:
        m.remove_unreferenced_vertices()
        m.fix_normals()
    except Exception:
        pass
    V=np.asarray(m.vertices,np.float64)
    F=np.asarray(m.faces,np.int32)
    return V,F

def _atlas_unit_scale(man):
    """Denver STL commonly uses millimetres. Infer one global unit scale only."""
    pts=[]
    for p in man.get("parts",[]):
        if p.get("kind")!="bone":
            continue
        try:
            V,_=_clean_mesh_master(p["path"])
            if len(V): pts.append(V[::max(1,len(V)//500)])
        except Exception:
            pass
    if not pts:
        return 1.0
    P=np.vstack(pts)
    span=float(np.max(np.ptp(P,axis=0)))
    # human lower limb should be O(1 m), not O(1000)
    return 0.001 if span>10.0 else 1.0

def _segment_frame_from_joints(J,nm,t,side,segment):
    """Rigid segment frame in SKEL coordinates."""
    if segment=="pelvis":
        pel=nm.get("pelvis"); hr=nm.get("femur_r"); hl=nm.get("femur_l")
        thor=nm.get("lumbar_body",nm.get("thorax"))
        o=J[t,pel]
        up=_unit(J[t,thor]-o,[0,1,0]) if thor is not None else np.array([0,1.,0])
        ml=_unit(J[t,hr]-J[t,hl],[1,0,0]) if hr is not None and hl is not None else np.array([1,0,0])
        ap=_unit(np.cross(ml,up),[0,0,1])
        ml=_unit(np.cross(up,ap),ml)
        B=np.stack([ml,ap,up],axis=1)
        L=float(np.linalg.norm(J[t,hr]-J[t,hl])) if hr is not None and hl is not None else .25
        return o,B,max(L,1e-6)
    if segment=="thigh":
        a=J[t,nm[f"femur_{side}"]]; b=J[t,nm[f"tibia_{side}"]]
    elif segment=="shank":
        a=J[t,nm[f"tibia_{side}"]]; b=J[t,nm[f"talus_{side}"]]
    else:
        a=J[t,nm.get(f"calcn_{side}",nm[f"talus_{side}"])]
        b=J[t,nm[f"toes_{side}"]]
    z=_unit(b-a,[0,-1,0])
    other=nm.get(f"femur_{'l' if side=='r' else 'r'}")
    hip=nm.get(f"femur_{side}")
    lr=(J[t,hip]-J[t,other]) if hip is not None and other is not None else np.array([1,0,0])
    x=lr-np.dot(lr,z)*z
    x=_unit(x,[1,0,0])
    y=_unit(np.cross(z,x),[0,0,1])
    x=_unit(np.cross(y,z),x)
    return np.asarray(a,float),np.stack([x,y,z],axis=1),max(float(np.linalg.norm(b-a)),1e-6)

def _master_donor_frame(man,side,segment,unit_scale):
    """One donor frame per anatomical segment, shared by every STL in it."""
    pref={
        "pelvis":["pelvis","sacrum"],
        "thigh":["femur"],
        "shank":["tibia"],
        "foot":["calcaneus","talus"],
    }[segment]
    cand=[p for p in man.get("parts",[]) if p.get("kind")=="bone"
          and p.get("region")==segment and p.get("side") in (side,None)]
    cand=sorted(cand,key=lambda p:(pref.index(p["name"]) if p["name"] in pref else 99,p["name"]))
    if not cand:
        return None
    # union of the key bone(s), still in the ORIGINAL shared Denver coordinates
    Vs=[]
    for p in cand[:2]:
        try:
            V,_=_clean_mesh_master(p["path"]); Vs.append(V*unit_scale)
        except Exception: pass
    if not Vs: return None
    V=np.vstack(Vs)
    C=np.mean(V,axis=0)
    B=_pca(V)
    spans=np.ptp((V-C)@B,axis=0)
    iz=int(np.argmax(spans))
    rem=[i for i in range(3) if i!=iz]
    z=B[:,iz]
    x=B[:,rem[0]]
    y=_unit(np.cross(z,x),B[:,rem[1]])
    x=_unit(np.cross(y,z),x)
    B=np.stack([x,y,z],axis=1)
    Q=(V-C)@B
    # proximal endpoint as shared segment origin
    o=C+B[:,2]*float(np.max(Q[:,2]))
    B[:,2]*=-1
    B[:,1]=_unit(np.cross(B[:,2],B[:,0]),B[:,1])
    L=max(float(np.ptp(Q[:,2])),1e-6)
    return o,B,L


def _simplify_connected_mesh(V,F,target_faces):
    """Simplifica manteniendo superficies conectadas; nunca muestrea caras aisladas."""
    V=np.asarray(V,np.float64)
    F=np.asarray(F,np.int32)
    m=trimesh.Trimesh(vertices=V,faces=F,process=True)
    if len(F)>int(target_faces):
        try:
            m=m.simplify_quadric_decimation(face_count=int(target_faces))
        except TypeError:
            m=m.simplify_quadric_decimation(int(target_faces))
        except Exception:
            pass
    try:
        m.remove_unreferenced_vertices()
        m.fix_normals()
    except Exception:
        pass
    return np.asarray(m.vertices,np.float32),np.asarray(m.faces,np.int32)

def _smoothstep01(x):
    x=np.clip(np.asarray(x,float),0.0,1.0)
    return x*x*(3.0-2.0*x)

def build_master_atlas(man,max_faces_each=60):
    """Preprocess Denver ONCE while preserving its shared anatomical coordinates."""
    sha=str(man.get("sha","unknown"))
    root=Path(man["root"])
    cache=root/f"master_atlas_v110_3_22_5_{max_faces_each}.npz"
    meta_path=root/f"master_atlas_v110_3_22_5_{max_faces_each}.json"
    if cache.exists() and meta_path.exists():
        d=np.load(cache,allow_pickle=True)
        return {
            "V":d["V"],"F":d["F"],"part_index":d["part_index"],
            "part_names":d["part_names"].tolist(),"part_sides":d["part_sides"].tolist(),
            "part_regions":d["part_regions"].tolist(),"unit_scale":float(d["unit_scale"][0]),
            "donor_frames":json.loads(meta_path.read_text(encoding="utf-8"))
        }

    us=_atlas_unit_scale(man)
    V_all=[]; F_all=[]; pidx=[]; names=[]; sides=[]; regions=[]; off=0
    muscle_parts=[p for p in man.get("parts",[]) if p.get("kind")=="muscle"]
    muscle_parts=sorted(muscle_parts,key=lambda p:(str(p.get("side")),p.get("name",""),p.get("path","")))
    for ip,p in enumerate(muscle_parts):
        V,F=_clean_mesh_master(p["path"])
        V=V*us
        if len(V)==0 or len(F)==0: continue
        Vs,Fs=_simplify_connected_mesh(V,F,max_faces_each)
        V_all.append(Vs.astype(np.float32)); F_all.append(Fs.astype(np.int32)+off)
        pidx.extend([len(names)]*len(Vs))
        names.append(p["name"]); sides.append(p.get("side") or "r"); regions.append(p.get("region") or "shank")
        off+=len(Vs)

    if not V_all:
        return None
    donor_frames={}
    for side in ("r","l"):
        for seg in ("pelvis","thigh","shank","foot"):
            ref=_master_donor_frame(man,side,seg,us)
            if ref is not None:
                o,B,L=ref
                donor_frames[f"{side}:{seg}"]={"o":np.asarray(o).tolist(),"B":np.asarray(B).tolist(),"L":float(L)}

    np.savez_compressed(
        cache,V=np.vstack(V_all).astype(np.float32),F=np.vstack(F_all).astype(np.int32),
        part_index=np.asarray(pidx,np.int16),
        part_names=np.asarray(names,dtype=object),part_sides=np.asarray(sides,dtype=object),
        part_regions=np.asarray(regions,dtype=object),unit_scale=np.asarray([us],np.float64)
    )
    meta_path.write_text(json.dumps(donor_frames,indent=2),encoding="utf-8")
    return {
        "V":np.vstack(V_all).astype(np.float32),"F":np.vstack(F_all).astype(np.int32),
        "part_index":np.asarray(pidx,np.int16),"part_names":names,"part_sides":sides,
        "part_regions":regions,"unit_scale":us,"donor_frames":donor_frames
    }

def _map_master_frame0(master,J,nm,skin0):
    """Register the master atlas ONCE to SKEL frame 0, segment-wise but coherently."""
    V0=np.asarray(master["V"],float)
    out=np.zeros_like(V0)
    seg_cache={}
    # target transform per side/segment
    for side in ("r","l"):
        for seg in ("pelvis","thigh","shank","foot"):
            key=f"{side}:{seg}"
            d=master["donor_frames"].get(key)
            if not d: continue
            do=np.asarray(d["o"],float); dB=np.asarray(d["B"],float); dL=float(d["L"])
            to,tB,tL=_segment_frame_from_joints(J,nm,0,side,seg)
            scale=tL/max(dL,1e-6)
            seg_cache[key]=(do,dB,to,tB,scale)

    # each muscle remains in the common Denver coordinate system and is transformed
    # using its anatomical chain; no independent PCA per STL.
    for ip,name in enumerate(master["part_names"]):
        side=master["part_sides"][ip] if master["part_sides"][ip] in ("r","l") else "r"
        region=master["part_regions"][ip]
        chain=MUSCLE_CHAIN.get(name,(region,region))
        idx=np.where(master["part_index"]==ip)[0]
        if len(idx)==0: continue
        P=V0[idx]
        k0=f"{side}:{chain[0]}"; k1=f"{side}:{chain[1]}"
        if k0 not in seg_cache: k0=f"{side}:{region}"
        if k1 not in seg_cache: k1=k0
        d0,B0,t0,T0,s0=seg_cache[k0]
        d1,B1,t1,T1,s1=seg_cache[k1]
        # map with both endpoint segment transforms and blend along muscle principal direction
        A=t0+((P-d0)@B0)*s0@T0.T if False else None
        P0=t0 + (((P-d0)@B0)*s0) @ T0.T
        P1=t1 + (((P-d1)@B1)*s1) @ T1.T
        if k0==k1:
            W=P0
        else:
            # weights derived from proximity to donor segment origins, preserving attachment ends
            dprox=np.linalg.norm(P-d0,axis=1)
            ddist=np.linalg.norm(P-d1,axis=1)
            w=dprox/(dprox+ddist+1e-9)
            w=np.clip(w,0.05,0.95)[:,None]
            W=(1-w)*P0+w*P1
        out[idx]=W
    return out,seg_cache

def _rigid_target_delta(J,nm,t,side,seg,base_frame):
    o0,B0,_=_segment_frame_from_joints(J,nm,0,side,seg)
    ot,Bt,_=_segment_frame_from_joints(J,nm,t,side,seg)
    R=Bt@B0.T
    return o0,ot,R


def _target_rigid_frame0_to_t(J,nm,t,side,seg,P):
    o0,B0,_=_segment_frame_from_joints(J,nm,0,side,seg)
    ot,Bt,_=_segment_frame_from_joints(J,nm,t,side,seg)
    R=Bt@B0.T
    return ot+(P-o0)@R.T

def _principal_coordinate(V):
    C=np.mean(V,axis=0)
    X=V-C
    try:
        _,_,vh=np.linalg.svd(X,full_matrices=False)
        axis=vh[0]
    except Exception:
        axis=np.array([0.0,0.0,1.0])
    q=X@axis
    return (q-np.min(q))/max(float(np.max(q)-np.min(q)),1e-12)

def _bounded_muscle_frame(V0,Vden,side,seg0,seg1,host,J,nm,t,donor_frames):
    Ph=_target_rigid_frame0_to_t(J,nm,t,side,host,V0)
    Pa=_target_rigid_frame0_to_t(J,nm,t,side,seg0,V0)
    Pb=_target_rigid_frame0_to_t(J,nm,t,side,seg1,V0)

    q=_principal_coordinate(Vden)
    da=donor_frames.get(f"{side}:{seg0}")
    db=donor_frames.get(f"{side}:{seg1}")
    if da and db:
        oa=np.asarray(da["o"],float)
        ob=np.asarray(db["o"],float)
        e0=np.mean(Vden[q<0.10],axis=0) if np.any(q<0.10) else Vden[np.argmin(q)]
        e1=np.mean(Vden[q>0.90],axis=0) if np.any(q>0.90) else Vden[np.argmax(q)]
        if np.linalg.norm(e0-oa)+np.linalg.norm(e1-ob) > np.linalg.norm(e1-oa)+np.linalg.norm(e0-ob):
            q=1.0-q

    # Central belly ~56% quasi-rigid; only terminal zones deform.
    wa=1.0-_smoothstep01(q/0.22)
    wb=_smoothstep01((q-0.78)/0.22)
    wh=np.clip(1.0-wa-wb,0.0,1.0)
    W=wh[:,None]*Ph + wa[:,None]*Pa + wb[:,None]*Pb

    # Shape preservation safeguard.
    dW=np.linalg.norm(np.ptp(W,axis=0))
    dH=np.linalg.norm(np.ptp(Ph,axis=0))
    ratio=dW/max(dH,1e-12)
    if ratio>1.18 or ratio<0.85:
        alpha=min(0.85,max(0.25,abs(ratio-1.0)))
        cW=np.mean(W,axis=0); cH=np.mean(Ph,axis=0)
        W=(1.0-alpha)*W + alpha*(Ph+(cW-cH))
    return W

def build_visible_human_muscle_sequence(man,joints,joint_names,skin_sequence,max_faces_each=900):
    """V110.3.22.9 — connected Denver muscle meshes + bounded skinning."""
    J=np.asarray(joints,np.float32)
    nm={str(n):i for i,n in enumerate(joint_names)}
    master=build_master_atlas(man,max_faces_each=max_faces_each)
    if master is None:
        return None,None

    Vden=np.asarray(master["V"],np.float32)
    F=np.asarray(master["F"],np.int32)
    V0=np.zeros_like(Vden,dtype=np.float32)
    host_by_part={}

    # Frame 0 morphology registration to one host segment, preserving each whole muscle.
    for ip,name in enumerate(master["part_names"]):
        side=master["part_sides"][ip] if master["part_sides"][ip] in ("r","l") else "r"
        region=master["part_regions"][ip]
        seg0,seg1=MUSCLE_CHAIN.get(name,(region,region))
        idx=np.where(master["part_index"]==ip)[0]
        if len(idx)==0:
            continue

        c=np.mean(Vden[idx],axis=0)
        def _dist(seg):
            d=master["donor_frames"].get(f"{side}:{seg}")
            return np.inf if not d else float(np.linalg.norm(c-np.asarray(d["o"],float)))
        host=seg0 if _dist(seg0)<=_dist(seg1) else seg1
        d=master["donor_frames"].get(f"{side}:{host}") or master["donor_frames"].get(f"{side}:{region}")
        if not d:
            V0[idx]=Vden[idx]
            host_by_part[ip]=region
            continue
        host_by_part[ip]=host

        do=np.asarray(d["o"],float)
        dB=np.asarray(d["B"],float)
        dL=max(float(d["L"]),1e-6)
        to,tB,tL=_segment_frame_from_joints(J,nm,0,side,host)
        sc=float(np.clip(tL/dL,0.35,3.0))
        V0[idx]=(to+(((Vden[idx]-do)@dB)*sc)@tB.T).astype(np.float32)

    frames=[V0.copy()]
    for t in range(1,len(J)):
        Vt=np.zeros_like(V0,dtype=np.float32)
        for ip,name in enumerate(master["part_names"]):
            side=master["part_sides"][ip] if master["part_sides"][ip] in ("r","l") else "r"
            region=master["part_regions"][ip]
            seg0,seg1=MUSCLE_CHAIN.get(name,(region,region))
            host=host_by_part.get(ip,region)
            idx=np.where(master["part_index"]==ip)[0]
            if len(idx)==0:
                continue
            try:
                if seg0==seg1:
                    Vt[idx]=_target_rigid_frame0_to_t(J,nm,t,side,host,V0[idx]).astype(np.float32)
                else:
                    Vt[idx]=_bounded_muscle_frame(
                        V0[idx],Vden[idx],side,seg0,seg1,host,J,nm,t,master["donor_frames"]
                    ).astype(np.float32)
            except Exception:
                Vt[idx]=_target_rigid_frame0_to_t(J,nm,t,side,host,V0[idx]).astype(np.float32)
        frames.append(Vt)

    return np.stack(frames,axis=0).astype(np.float32),F
