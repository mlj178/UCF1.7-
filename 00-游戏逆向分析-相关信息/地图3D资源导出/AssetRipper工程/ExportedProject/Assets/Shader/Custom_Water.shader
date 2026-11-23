Shader "Custom/Water" {
	Properties {
		[HideInInspector] _EmissionColor ("Emission Color", Vector) = (1,1,1,1)
		[HideInInspector] _AlphaCutoff ("Alpha Cutoff ", Range(0, 1)) = 0.5
		[ASEBegin] _DistanceFade ("Distance Fade", Float) = 1000
		_DistanceFadeOffset ("Distance Fade Offset", Float) = 500
		[Space(10)] [Header(Main Parameters)] [Space(10)] _NormalMap ("Normal", 2D) = "bump" {}
		_NormalPower ("Normal Power", Range(0, 1)) = 1
		_RefractionPower ("Refraction Power", Range(0, 5)) = 1
		_NormalScale ("Normal Scale", Float) = 1
		_NormalSpeed ("Normal Speed", Float) = 0.1
		_NormalDirection ("Normal Direction", Vector) = (1,0,-1,0.2)
		[Space(10)] [Header(Foam)] [Space(10)] _FoamMask ("Foam Mask", 2D) = "white" {}
		_FoamNormal ("Foam Normal", 2D) = "bump" {}
		_FoamDistance ("Foam Distance", Range(0, 100)) = 1
		_FoamPower ("Foam Power", Range(0, 1)) = 1
		_FoamScale ("Foam Scale", Float) = 1
		_FoamContrast ("Foam Contrast", Float) = 0
		_FoamSpeed ("Foam Speed", Float) = 0.1
		[Space(30)] _EdgesFade ("Edges Fade", Float) = 0.1
		_DepthColor1 ("Shallow Color (RGBA)", Vector) = (0,0.6810271,0.6886792,1)
		_DepthColor ("Depth Color (RGBA)", Vector) = (0,0.6810271,0.6886792,1)
		_Depth ("Depth", Float) = 1
		[Space(30)] _CausticsColor ("Caustics Color", Vector) = (0.5404058,0.8679245,0.8414827,1)
		_CausticsScale ("Caustics Scale", Float) = 0.5
		_CausticsSpeed ("Caustics Speed", Float) = 2
		[Space(30)] _WavesHeight ("Waves Height", Float) = 25
		_WavesSpeed ("Waves Speed", Float) = 5
		_WavesScale ("Waves Scale", Float) = 10
		[Space(10)] [Header(Metallic Smoothness)] [Space(10)] _MetallicPower ("Metallic Power", Range(0, 1)) = 1
		[ASEEnd] _SmoothnessPower ("Smoothness Power", Range(0, 1)) = 1
	}
	//DummyShaderTextExporter
	SubShader{
		Tags { "RenderType" = "Opaque" }
		LOD 200

		Pass
		{
			HLSLPROGRAM
			#pragma vertex vert
			#pragma fragment frag

			float4x4 unity_ObjectToWorld;
			float4x4 unity_MatrixVP;

			struct Vertex_Stage_Input
			{
				float4 pos : POSITION;
			};

			struct Vertex_Stage_Output
			{
				float4 pos : SV_POSITION;
			};

			Vertex_Stage_Output vert(Vertex_Stage_Input input)
			{
				Vertex_Stage_Output output;
				output.pos = mul(unity_MatrixVP, mul(unity_ObjectToWorld, input.pos));
				return output;
			}

			float4 frag(Vertex_Stage_Output input) : SV_TARGET
			{
				return float4(1.0, 1.0, 1.0, 1.0); // RGBA
			}

			ENDHLSL
		}
	}
	Fallback "Hidden/InternalErrorShader"
	//CustomEditor "UnityEditor.ShaderGraph.PBRMasterGUI"
}