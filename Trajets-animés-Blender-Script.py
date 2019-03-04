# -*- coding: utf-8 -*-

try:
    import bpy, bmesh
except:
    pass
    
import csv
import math
import struct 
import copy
import random
import numpy as np

print("---------------------")

showShapefile, showAnimation, EraseShapefile, EraseAnimation = False,True,False,True
EraseText = True

ShapefileName = '/Volumes/Seagate Backup Plus Drive/Departement_de_geo/3d/TrajetsMontréal/shapeFileHeat.csv'
ShapefileNameSimple = '/Volumes/Seagate Backup Plus Drive/Departement_de_geo/3d/TrajetsMontréal/shapeFile.csv'
colourDiv = ['#4487a4','#61859a','#7a828e','#8b8084','#9b7d79','#a77b70','#b47765','#bf745b','#cd6f4e','#d76b44','#e16638','#ec602a']

def rect2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2rect(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)
    


def cylinder_between(x1, y1, z1, x2, y2, z2, r1, r2, col, l):

    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    
    bpy.ops.mesh.primitive_cone_add(
        radius1=r1,
        radius2=r2,
        depth=dist,
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1),
        end_fill_type = 'NGON'
    )
    
    obj = bpy.context.object
    
    if l == 'Legend':
        obj.name = 'legend_object'
    else:
        obj.name = 'edge'
    
    obj.cycles_visibility.shadow = True

    phi = math.atan2(dy, dx) 
    theta = math.acos(dz/dist) 

    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi
    
#    print(col,len(bpy.context.object.material_slots))
    
    # Assign it to object
    if bpy.context.object.data.materials:
        # assign to 1st material slot
        bpy.context.object.data.materials[0] = bpy.data.materials[col]
    else:
        # no slots
        bpy.context.object.data.materials.append(bpy.data.materials[col])
    
    obj.cycles_visibility.shadow = True

def displayAnimation(fileName):
    
    z1,z2 = 1150,1150
    
    center = (-73.7179, 45.55495)

    orig_lon = center[0]
    orig_lat = -center[1]
    csvfile = open(ShapefileNameSimple)
    S = csv.reader(csvfile, delimiter=',', quotechar='"')
    S = list(S)
    print(len(S))
    
    c = 0
    for s in S:
        
        c += 1
        
        #Not the most efficient way of creating a mesh , but should be fine for just one object
#        bpy.ops.mesh.primitive_uv_sphere_add(size=1)
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions = 2,
            size = 120)
        ball = bpy.context.object
        ball.name = 'ball'
        col = int((255 - 50)/250*9)
        print(c)
        if bpy.context.object.data.materials:
            # assign to 1st material slot
            bpy.context.object.data.materials[0] = bpy.data.materials['white']
        else:
            # no slots
            bpy.context.object.data.materials.append(bpy.data.materials['white'])
        
        obj.cycles_visibility.shadow = True

        startFrame = random.randint(0,30)
        increment = 5 #This can also be in the csv
        newFrame = startFrame
        
        verts = []
        for ll in range(1,len(s)):
            pt = []
            for t in s[ll].replace('(','').replace(')','').split(', '):
                pt.append(float(t))
            verts.append(pt)
            
        sens = random.random()
        
        if sens > .5:
            for ii in range(5):
                
                newFrame += random.randint(-10,10)
                
                dist = 0
                for i in range(len(verts)-1):
                    
                    v1 = verts[len(verts)-1-i-1]
                    v2 = verts[len(verts)-1-i]
                    
                    v2[1] = -v2[1]
                    
                    if v2[1] > 0:
                        v2[1] = -v2[1]
                        
                    if v1[1] > 0:
                        v1[1] = -v1[1]
                        
                    x1 = 1000 * (v1[0]-orig_lon)*40000*math.cos((orig_lat+v1[1])*math.pi/360)/360
                    y1 = 1000 * (orig_lat-v1[1])*40000/360
                    
                    x2 = 1000 * (v2[0]-orig_lon)*40000*math.cos((orig_lat+v2[1])*math.pi/360)/360
                    y2 = 1000 * (orig_lat-v2[1])*40000/360
                    
        #            print(x1,y1,x2,y2)
                    
                    dx = x2 - x1
                    dy = y2 - y1
                    dz = z2 - z1 
                    dist += math.sqrt(dx**2 + dy**2 + dz**2)
                
                for i in range(len(verts)-1):
                    
                    v1 = verts[i]
                    v2 = verts[i+1]
                    
                    v2[1] = -v2[1]
                    
                    if v2[1] > 0:
                        v2[1] = -v2[1]
                        
                    if v1[1] > 0:
                        v1[1] = -v1[1]
                        
                    x1 = 1000 * (v1[0]-orig_lon)*40000*math.cos((orig_lat+v1[1])*math.pi/360)/360
                    y1 = 1000 * (orig_lat-v1[1])*40000/360
                    
                    x2 = 1000 * (v2[0]-orig_lon)*40000*math.cos((orig_lat+v2[1])*math.pi/360)/360
                    y2 = 1000 * (orig_lat-v2[1])*40000/360
                    
        #            print(x1,y1,x2,y2)
                    
                    dx = x2 - x1
                    dy = y2 - y1
                    dz = z2 - z1 
                    dist1 = math.sqrt(dx**2 + dy**2 + dz**2)
                    
                    ball.location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)
                    ball.keyframe_insert(data_path='location', frame = newFrame)
                    
                    for fcurve in ball.animation_data.action.fcurves:
                        kf = fcurve.keyframe_points[-1]
                        kf.interpolation = 'LINEAR'
                    
                    newFrame += 50 * (dist1/dist)
    #                newFrame += (dist/len(verts))/1000
                for i in range(len(verts)-1):
                    
                    v1 = verts[len(verts)-1-i-1]
                    v2 = verts[len(verts)-1-i]
                    
                    v2[1] = -v2[1]
                    
                    if v2[1] > 0:
                        v2[1] = -v2[1]
                        
                    if v1[1] > 0:
                        v1[1] = -v1[1]
                        
                    x1 = 1000 * (v1[0]-orig_lon)*40000*math.cos((orig_lat+v1[1])*math.pi/360)/360
                    y1 = 1000 * (orig_lat-v1[1])*40000/360
                    
                    x2 = 1000 * (v2[0]-orig_lon)*40000*math.cos((orig_lat+v2[1])*math.pi/360)/360
                    y2 = 1000 * (orig_lat-v2[1])*40000/360
                    
        #            print(x1,y1,x2,y2)
                    
                    dx = x2 - x1
                    dy = y2 - y1
                    dz = z2 - z1 
                    dist1 = math.sqrt(dx**2 + dy**2 + dz**2)
                    
                    ball.location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)
                    ball.keyframe_insert(data_path='location', frame = newFrame)
                    
                    for fcurve in ball.animation_data.action.fcurves:
                            kf = fcurve.keyframe_points[-1]
                            kf.interpolation = 'LINEAR'
                            
                    newFrame += 50 * (dist1/dist)
    #                print(dist/dist1) 
    #               newFrame += (dist/len(verts))/1000
                newFrame += 50 * 2
        else:
            for ii in range(5):
                
                newFrame += random.randint(-10,10)
                
                dist = 0
                for i in range(len(verts)-1):
                    
                    v1 = verts[len(verts)-1-i-1]
                    v2 = verts[len(verts)-1-i]
                    
                    v2[1] = -v2[1]
                    
                    if v2[1] > 0:
                        v2[1] = -v2[1]
                        
                    if v1[1] > 0:
                        v1[1] = -v1[1]
                        
                    x1 = 1000 * (v1[0]-orig_lon)*40000*math.cos((orig_lat+v1[1])*math.pi/360)/360
                    y1 = 1000 * (orig_lat-v1[1])*40000/360
                    
                    x2 = 1000 * (v2[0]-orig_lon)*40000*math.cos((orig_lat+v2[1])*math.pi/360)/360
                    y2 = 1000 * (orig_lat-v2[1])*40000/360
                    
        #            print(x1,y1,x2,y2)
                    
                    dx = x2 - x1
                    dy = y2 - y1
                    dz = z2 - z1 
                    dist += math.sqrt(dx**2 + dy**2 + dz**2)
                
                for i in range(len(verts)-1):

                    
                    v1 = verts[len(verts)-1-i-1]
                    v2 = verts[len(verts)-1-i]
                    
                    v2[1] = -v2[1]
                    
                    if v2[1] > 0:
                        v2[1] = -v2[1]
                        
                    if v1[1] > 0:
                        v1[1] = -v1[1]
                        
                    x1 = 1000 * (v1[0]-orig_lon)*40000*math.cos((orig_lat+v1[1])*math.pi/360)/360
                    y1 = 1000 * (orig_lat-v1[1])*40000/360
                    
                    x2 = 1000 * (v2[0]-orig_lon)*40000*math.cos((orig_lat+v2[1])*math.pi/360)/360
                    y2 = 1000 * (orig_lat-v2[1])*40000/360
                    
        #            print(x1,y1,x2,y2)
                    
                    dx = x2 - x1
                    dy = y2 - y1
                    dz = z2 - z1 
                    dist1 = math.sqrt(dx**2 + dy**2 + dz**2)
                    
                    ball.location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)
                    ball.keyframe_insert(data_path='location', frame = newFrame)
                    
                    for fcurve in ball.animation_data.action.fcurves:
                        kf = fcurve.keyframe_points[-1]
                        kf.interpolation = 'LINEAR'
                    
                    newFrame += 75 * (dist1/dist)
    #                newFrame += (dist/len(verts))/1000
                for i in range(len(verts)-1):
                    

                    
                    v1 = verts[i]
                    v2 = verts[i+1]
                    
                    v2[1] = -v2[1]
                    
                    if v2[1] > 0:
                        v2[1] = -v2[1]
                        
                    if v1[1] > 0:
                        v1[1] = -v1[1]
                        
                    x1 = 1000 * (v1[0]-orig_lon)*40000*math.cos((orig_lat+v1[1])*math.pi/360)/360
                    y1 = 1000 * (orig_lat-v1[1])*40000/360
                    
                    x2 = 1000 * (v2[0]-orig_lon)*40000*math.cos((orig_lat+v2[1])*math.pi/360)/360
                    y2 = 1000 * (orig_lat-v2[1])*40000/360
                    
        #            print(x1,y1,x2,y2)
                    
                    dx = x2 - x1
                    dy = y2 - y1
                    dz = z2 - z1 
                    dist1 = math.sqrt(dx**2 + dy**2 + dz**2)
                    
                    ball.location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)
                    ball.keyframe_insert(data_path='location', frame = newFrame)
                    
                    for fcurve in ball.animation_data.action.fcurves:
                            kf = fcurve.keyframe_points[-1]
                            kf.interpolation = 'LINEAR'
                            
                    newFrame += 75 * (dist1/dist)
    #                print(dist/dist1) 
    #               newFrame += (dist/len(verts))/1000
                newFrame += 50 * 2
    

def displayShapeFile(fileName):
    
    center = (-73.7179, 45.55495)

    orig_lon = center[0]
    orig_lat = -center[1]
    
    csvfile = open(ShapefileName)
    S = csv.reader(csvfile, delimiter=',', quotechar='"')
    S = list(S)
    
    c = 0
    for s in S:
        verts = []
        for ll in range(1,len(s)):
            pt = []
            for t in s[ll].replace('[','').replace(']','').split(', '):
                pt.append(float(t))
            verts.append(pt)
        
        for i in range(len(verts)-1):
            
            
            
            v1 = verts[i]
            v2 = verts[i+1]
            
#            print(v1,v2)
            #print(v1,orig_lon,v2,orig_lat)
    #        v1[1] = -v1[1]
            v2[1] = -v2[1]
            
            if v2[1] > 0:
                v2[1] = -v2[1]
                
            if v1[1] > 0:
                v1[1] = -v1[1]
                
            x1 = 1000 * (v1[0]-orig_lon)*40000*math.cos((orig_lat+v1[1])*math.pi/360)/360
            y1 = 1000 * (orig_lat-v1[1])*40000/360
            
            x2 = 1000 * (v2[0]-orig_lon)*40000*math.cos((orig_lat+v2[1])*math.pi/360)/360
            y2 = 1000 * (orig_lat-v2[1])*40000/360
            
            #print(i,x1, y1, 1000, x2, y2, 1000, 30)
#            print(v1[2],v2[2])
            if v1[2] >= v2[2]:
                col = int((255 - v1[2])/250*9)
            else:
                col = int((255 - v2[2])/250*9)
            
            col = int(((255 - v1[2])/250*9 + (255 - v2[2])/250*9)/2)
            print('Display Shapefile',c,"col:",col,v1[2],v2[2])
#            print()
#            print(c,len(S),v1[2], v2[2], col)
#            print(x1, y1)
            cylinder_between(x1, y1, 1000, x2, y2, 1000, 255 - v1[2], 255 - v2[2], colourDiv[col], 'edge')
            
        c += 1
            
#        if c > 20:
#            break
        
        
#    bm.faces.new(bm.verts)
#
#    bm.normal_update()
#
#    me = bpy.data.meshes.new("ccc")
#    bm.to_mesh(me)
#    
#    ob = bpy.data.objects.new("ccc", me)
#    bpy.context.scene.objects.link(ob)
#    bpy.context.scene.update()
#    
try:
    
    if EraseText:
        #remove texts
        for obj in bpy.data.objects:
            obj.select = False
        bpy.ops.object.select_pattern(pattern="text*")
        bpy.ops.object.delete()
        
        #remove texts
        for obj in bpy.data.objects:
            obj.select = False
        bpy.ops.object.select_pattern(pattern="Decile_text*")
        bpy.ops.object.delete()
        
        for obj in bpy.data.objects:
            obj.select = False
        bpy.ops.object.select_pattern(pattern="Map_title*")
        bpy.ops.object.delete()
        
        for obj in bpy.data.objects:
            obj.select = False
        bpy.ops.object.select_pattern(pattern="Decile_title*")
        bpy.ops.object.delete()
    
    if EraseShapefile:
        for obj in bpy.data.objects:
            obj.select = False
        bpy.ops.object.select_pattern(pattern="edge*")
        bpy.ops.object.delete()
    
    if EraseAnimation:
        for obj in bpy.data.objects:
            obj.select = False
        bpy.ops.object.select_pattern(pattern="ball*")
        bpy.ops.object.delete()
    
    for obj in bpy.data.objects:
        obj.select = False
    bpy.ops.object.select_pattern(pattern="legend_object*")
    bpy.ops.object.delete()
    
    
except:
    pass

if showShapefile:
    displayShapeFile(ShapefileName)

if showAnimation:
    displayAnimation(ShapefileNameSimple)

def makeLegend(deciles,maxVar):
    
    print('making legend')

#    #titre Carte
    bpy.ops.object.text_add(location=(-0000, 17100, 610),rotation = (math.radians(0),0,math.radians(0)))
    te2 = bpy.context.object
    fnt = bpy.data.fonts.load('/Volumes/Seagate Backup Plus Drive/Departement_de_geo/3d/montreal3/AkkRg_Pro.ttf')
    te2.data.font = fnt
    te2.data.align_x = 'CENTER'
    
    te2.data.body = 'SUPERPOSITION DES TRACÉS SUGGÉRÉS PAR LES\nPARTICIPANTS DES ATELIERS CONSULTATIONS PUBLIQUES'
    
    te2.scale = (900,900,900)
    
    te2.cycles_visibility.shadow = False
    
    te2.data.materials.append(bpy.data.materials.get("Material.noir"))
    
    obj = bpy.context.object
    obj.name = 'Map_title'
#    bpy.data.curves['Text.346'].space_character = 1.2
    
    #titre Légende
    bpy.ops.object.text_add(location=(-20000, 15700, 610),rotation = (math.radians(0),0,math.radians(0)))
    te2 = bpy.context.object
    fnt = bpy.data.fonts.load('/Volumes/Seagate Backup Plus Drive/Departement_de_geo/3d/montreal3/AkkRg_Pro.ttf')
    te2.data.font = fnt
    te2.data.align_x = 'CENTER'
    
    te2.data.body = 'Légende'
    
    te2.scale = (750,750,750)
    
    te2.cycles_visibility.shadow = False
    
    te2.data.materials.append(bpy.data.materials.get("Material.noir"))
    
    obj = bpy.context.object
    obj.name = 'Map_title'
    
    
    dec_count = 0
    for dec in deciles:
        
        bpy.ops.object.text_add(location=(-19900, 6800 + dec_count * 800, 610),rotation = (math.radians(0),0,math.radians(0)))
#        print(14000 - dec_count * 800)
        te2 = bpy.context.object
        fnt = bpy.data.fonts.load('/Volumes/Seagate Backup Plus Drive/Departement_de_geo/3d/montreal3/AkkRg_Pro.ttf')
        te2.data.font = fnt
        te2.data.align_x = 'LEFT'
        if dec > 0:
            texte = ' tracés'
        else:
            texte = ' tracé'
        try:
            te2.data.body = str(int(dec+1)) + texte#'De ' + str(int(dec)) + '$ à ' + str(int(deciles[dec_count+1])) + '$'
        except:
            te2.data.body = ''#'De ' + str(int(dec)) + '$ à ' + str(int(maxVar)) + '$'
        
        print(dec_count,str(int(dec+1)) + texte, 6800 + dec_count * 800)
        
        te2.scale = (500,500,500)
        
        te2.data.materials.append(bpy.data.materials.get("Material.noir"))
        te2.cycles_visibility.shadow = False
        
        obj = bpy.context.object
        obj.name = 'Decile_text'
        
        col = colourDiv[dec]
        print(dec_count,col, 6800 + 140 + (dec_count) * 800,255 - int((9-dec)/10*255))
        print()
#        print(-20000, 14000 - dec_count * 800, 610, -20000, 14000 - dec_count * 800, 610, 255 - int(dec/12*255), 255 - int(dec/12*255), col, 'Legend')
        cylinder_between(-21500, 6800 + 140 + (dec_count) * 800, 1000, -20200, 6800 + 140 + (dec_count) * 800, 1000, 255 - int((9-dec)/10*255), 255 - int((9-dec)/10*255), col, 'Legend')

        dec_count += 1

makeLegend([0,1,2,3,4,5,6,7,8],12)
