using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public class UcfBuild
{
    const string Root = "D:/ucf_unity";
    const string FbxAsset = "Assets/Models/ForbiddenTD_Classic.fbx";
    const string TexDir = "Assets/Textures";
    const string GrpDir = "Assets/Merged";
    const string ScenePath = "Assets/Scenes/TestMap12.unity";
    const string BuildDir = "D:/ucf_unity/build";
    const string ExePath = "D:/ucf_unity/build/UcfTest.exe";

    static StringBuilder SB = new StringBuilder();
    static Dictionary<string, Texture2D> TexByName = new Dictionary<string, Texture2D>();

    static void L(string s)
    {
        SB.AppendLine(s);
        Debug.Log("[UCFBUILD] " + s);
        try { File.WriteAllText(Root + "/build_log.txt", SB.ToString()); } catch (Exception) { }
    }

    static string Norm(string s)
    {
        if (string.IsNullOrEmpty(s)) return "";
        StringBuilder sb = new StringBuilder();
        foreach (char c in s.ToLowerInvariant())
            if ((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')) sb.Append(c);
        return sb.ToString();
    }

    static void LoadTexIndex()
    {
        foreach (string g in AssetDatabase.FindAssets("t:Texture2D", new string[] { TexDir }))
        {
            Texture2D t = AssetDatabase.LoadAssetAtPath<Texture2D>(AssetDatabase.GUIDToAssetPath(g));
            if (t == null) continue;
            string k = Norm(t.name);
            if (!TexByName.ContainsKey(k)) TexByName[k] = t;
        }
        L("textures indexed = " + TexByName.Count);
    }

    static Bounds GetBounds(GameObject go)
    {
        Renderer[] rs = go.GetComponentsInChildren<Renderer>();
        if (rs.Length == 0) return new Bounds(Vector3.zero, Vector3.zero);
        Bounds b = rs[0].bounds;
        for (int i = 1; i < rs.Length; i++) b.Encapsulate(rs[i].bounds);
        return b;
    }

    public static void Build()
    {
        try
        {
            L("STEP=start");
            PlayerSettings.companyName = "UcfTest";
            PlayerSettings.productName = "UcfTest";
            PlayerSettings.colorSpace = ColorSpace.Linear;

            AssetImporter ai = AssetImporter.GetAtPath(FbxAsset);
            if (ai == null) { L("FATAL fbx missing"); return; }
            ModelImporter mi = (ModelImporter)ai;
            mi.globalScale = 1f;
            mi.useFileScale = true;
            mi.importAnimation = false;
            mi.animationType = ModelImporterAnimationType.None;
            mi.importCameras = false;
            mi.importLights = false;
            mi.importBlendShapes = false;
            mi.importVisibility = false;
            mi.importNormals = ModelImporterNormals.Import;
            mi.importTangents = ModelImporterTangents.None;
            mi.meshCompression = ModelImporterMeshCompression.Off;
            mi.optimizeMeshPolygons = false;
            mi.optimizeMeshVertices = false;
            mi.weldVertices = false;
            mi.isReadable = true;
            mi.materialImportMode = ModelImporterMaterialImportMode.ImportStandard;
            mi.SaveAndReimport();
            AssetDatabase.Refresh();
            LoadTexIndex();

            GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(FbxAsset);
            if (prefab == null) { L("FATAL prefab null"); return; }

            if (!AssetDatabase.IsValidFolder(GrpDir))
                AssetDatabase.CreateFolder("Assets", "Merged");
            string[] old = AssetDatabase.FindAssets("", new string[] { GrpDir });
            foreach (string g in old) AssetDatabase.DeleteAsset(AssetDatabase.GUIDToAssetPath(g));
            AssetDatabase.Refresh();

            // ---------- pass 1: merge ----------
            Scene tmp = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            GameObject root = UnityEngine.Object.Instantiate(prefab);
            root.name = "Src";
            root.transform.position = Vector3.zero;
            root.transform.rotation = Quaternion.identity;
            root.transform.localScale = Vector3.one;

            Bounds b0 = GetBounds(root);
            float maxDim = Mathf.Max(b0.size.x, b0.size.y, b0.size.z);
            if (maxDim > 0.001f)
            {
                float factor = 175f / maxDim;
                if (factor < 0.95f || factor > 1.05f) root.transform.localScale = root.transform.localScale * factor;
                L("scale factor=" + factor.ToString("F5"));
            }
            Bounds b1 = GetBounds(root);
            root.transform.position = root.transform.position + new Vector3(-b1.center.x, -b1.min.y, -b1.center.z);
            Physics.SyncTransforms();
            Bounds b2 = GetBounds(root);
            L("modelBounds min=" + b2.min.ToString("F2") + " max=" + b2.max.ToString("F2"));

            MeshFilter[] mfs = root.GetComponentsInChildren<MeshFilter>();
            Dictionary<string, List<MeshFilter>> groups = new Dictionary<string, List<MeshFilter>>();
            foreach (MeshFilter mf in mfs)
            {
                MeshRenderer mr = mf.GetComponent<MeshRenderer>();
                string src = (mr != null && mr.sharedMaterial != null) ? Norm(mr.sharedMaterial.name) : "none";
                if (!groups.ContainsKey(src)) groups[src] = new List<MeshFilter>();
                groups[src].Add(mf);
            }
            List<string> keys = new List<string>(groups.Keys);
            keys.Sort();
            L("STEP=grouped groups=" + keys.Count);

            Shader unlitTex = Shader.Find("Unlit/Texture");
            Shader unlitCol = Shader.Find("Unlit/Color");
            L("shaders tex=" + (unlitTex != null) + " col=" + (unlitCol != null));

            int okGroups = 0;
            foreach (string key in keys)
            {
                List<MeshFilter> list = groups[key];
                CombineInstance[] ci = new CombineInstance[list.Count];
                for (int i = 0; i < list.Count; i++)
                {
                    ci[i].mesh = list[i].sharedMesh;
                    ci[i].transform = list[i].transform.localToWorldMatrix;
                }
                Mesh m = new Mesh();
                m.indexFormat = UnityEngine.Rendering.IndexFormat.UInt32;
                try
                {
                    m.CombineMeshes(ci, true, true);
                }
                catch (Exception e)
                {
                    L("WARN combine fail " + key + " " + e.Message);
                    continue;
                }
                m.name = "GRP_" + key;
                m.RecalculateBounds();
                AssetDatabase.CreateAsset(m, GrpDir + "/GRP_" + key + ".asset");

                Material mat = new Material(unlitTex != null ? unlitTex : unlitCol);
                mat.name = "GRP_" + key;
                Texture2D tex;
                if (TexByName.TryGetValue(key, out tex)) { mat.mainTexture = tex; mat.color = Color.white; }
                else { mat.mainTexture = null; mat.color = new Color(0.8f, 0.8f, 0.82f, 1f); }
                AssetDatabase.CreateAsset(mat, GrpDir + "/M_GRP_" + key + ".mat");
                okGroups++;
            }
            L("STEP=merged ok=" + okGroups + " of " + keys.Count);

            UnityEngine.Object.DestroyImmediate(root);
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            // ---------- pass 2: final scene ----------
            Scene scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);

            Material groundMat = new Material(unlitCol != null ? unlitCol : unlitTex);
            groundMat.name = "GRP_zzground";
            groundMat.color = new Color(0.42f, 0.40f, 0.38f, 1f);
            AssetDatabase.CreateAsset(groundMat, GrpDir + "/M_GRP_zzground.mat");

            List<string> allKeys = new List<string>(keys);
            allKeys.Add("zzground");

            int made = 0;
            foreach (string key in allKeys)
            {
                Mesh mesh;
                Material mat;
                if (key == "zzground")
                {
                    mesh = new Mesh();
                    mesh.name = "GRP_zzground";
                    float h = 400f;
                    float dep = 12f;
                    Vector3[] v = {
                        new Vector3(-h, 0, -h), new Vector3(-h, 0, h), new Vector3(h, 0, h), new Vector3(h, 0, -h),
                        new Vector3(-h, -dep, -h), new Vector3(-h, -dep, h), new Vector3(h, -dep, h), new Vector3(h, -dep, -h)
                    };
                    int[] t = {
                        0,1,2, 0,2,3,
                        4,7,6, 4,6,5,
                        0,3,7, 0,7,4,
                        1,5,6, 1,6,2,
                        2,6,7, 2,7,3,
                        0,4,5, 0,5,1
                    };
                    Vector2[] uv = new Vector2[8];
                    for (int ui = 0; ui < 8; ui++) uv[ui] = new Vector2(v[ui].x * 0.01f, v[ui].z * 0.01f);
                    mesh.vertices = v;
                    mesh.uv = uv;
                    mesh.triangles = t;
                    mesh.RecalculateNormals();
                    mesh.RecalculateBounds();
                    AssetDatabase.CreateAsset(mesh, GrpDir + "/GRP_zzground.asset");
                    mat = groundMat;
                }
                else
                {
                    mesh = AssetDatabase.LoadAssetAtPath<Mesh>(GrpDir + "/GRP_" + key + ".asset");
                    mat = AssetDatabase.LoadAssetAtPath<Material>(GrpDir + "/M_GRP_" + key + ".mat");
                }
                if (mesh == null) { L("WARN missing mesh " + key); continue; }

                GameObject go = new GameObject("GRP_" + key);
                go.transform.position = Vector3.zero;
                go.transform.rotation = Quaternion.identity;
                go.transform.localScale = Vector3.one;
                MeshFilter filter = go.AddComponent<MeshFilter>();
                filter.sharedMesh = mesh;
                MeshRenderer rend = go.AddComponent<MeshRenderer>();
                rend.sharedMaterial = mat;
                MeshCollider cl = go.AddComponent<MeshCollider>();
                cl.sharedMesh = mesh;
                cl.convex = false;
                made++;
            }
            L("STEP=scene objects=" + made);

            GameObject sunGO = new GameObject("Sun");
            Light sun = sunGO.AddComponent<Light>();
            sun.type = LightType.Directional;
            sun.intensity = 1.2f;
            sunGO.transform.rotation = Quaternion.Euler(50f, -32f, 0f);
            RenderSettings.ambientMode = UnityEngine.Rendering.AmbientMode.Flat;
            RenderSettings.ambientLight = new Color(0.45f, 0.47f, 0.5f, 1f);
            RenderSettings.fog = false;
            RenderSettings.skybox = null;

            GameObject camGO = new GameObject("Main Camera");
            camGO.tag = "MainCamera";
            Camera cam = camGO.AddComponent<Camera>();
            cam.fieldOfView = 67.5f;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0f, 1f, 0f, 1f);
            camGO.AddComponent<AudioListener>();
            camGO.transform.position = new Vector3(0f, 95f, -175f);
            camGO.transform.LookAt(new Vector3(0f, 22f, 0f));

            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene, ScenePath);

            EditorBuildSettings.scenes = new EditorBuildSettingsScene[] { new EditorBuildSettingsScene(ScenePath, true) };

            Directory.CreateDirectory(BuildDir);
            BuildPlayerOptions opts = new BuildPlayerOptions();
            opts.scenes = new string[] { ScenePath };
            opts.locationPathName = ExePath;
            opts.target = BuildTarget.StandaloneWindows;
            opts.options = BuildOptions.None;
            L("STEP=building");
            BuildReport rpt = BuildPipeline.BuildPlayer(opts);
            L("STEP=builddone " + rpt.summary.result + " errors=" + rpt.summary.totalErrors);

            string dataDir = BuildDir + "/UcfTest_Data";
            if (Directory.Exists(dataDir))
                foreach (string f in Directory.GetFiles(dataDir))
                    L("OUT " + Path.GetFileName(f) + " " + new FileInfo(f).Length);
            L("STEP=END");
        }
        catch (Exception e)
        {
            L("FATAL " + e.ToString());
        }
    }
}
