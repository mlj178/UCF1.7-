Shader "CrossFire/PVModelDefault" {
	Properties {
		[HideInInspector] _EmissionColor ("Emission Color", Vector) = (1,1,1,1)
		[HideInInspector] _AlphaCutoff ("Alpha Cutoff ", Range(0, 1)) = 0.5
		[ASEBegin] _MainTex ("MainTex", 2D) = "white" {}
		[Toggle(_DISABLENORMALMAP_ON)] _DisableNormalMap ("DisableNormalMap", Float) = 0
		_NormalScale ("NormalScale", Range(0, 10)) = 1
		[Normal] _NormalMap ("NormalMap", 2D) = "white" {}
		_SpecularMap ("SpecularMap", 2D) = "white" {}
		_AlphaMap ("AlphaMap", 2D) = "white" {}
		_CubeMap ("CubeMap", Cube) = "white" {}
		_BaseColor ("BaseColor", Vector) = (1,1,1,1)
		_MainBrightness ("MainBrightness", Float) = 1
		_SpecularBrightness ("SpecularBrightness", Float) = 1
		_CubeMapBrightness ("CubeMapBrightness", Float) = 1
		_MinDiffuse ("MinDiffuse", Range(0, 1)) = 0.5
		_MinShadow ("MinShadow", Range(0, 1)) = 0.5
		_MinSpecular ("MinSpecular", Range(0, 1)) = 0
		_Gloss ("Gloss", Range(0, 10)) = 1
		_MinAlpha ("MinAlpha", Range(0, 1)) = 0
		[Toggle(_DISABLEDALPHAR_ON)] _DisabledAlphaR ("DisabledAlphaR", Float) = 0
		[Enum(UnityEngine.Rendering.BlendMode)] _RGBSrc ("RGBSrc", Float) = 1
		[Enum(UnityEngine.Rendering.BlendMode)] _RGBDst ("RGBDst", Float) = 0
		[Enum(UnityEngine.Rendering.BlendMode)] _AlphaSrc ("AlphaSrc", Float) = 1
		[ASEEnd] [Enum(UnityEngine.Rendering.BlendMode)] _AlphaDst ("AlphaDst", Float) = 0
		[HideInInspector] _texcoord ("", 2D) = "white" {}
	}
	//DummyShaderTextExporter
	SubShader{
		Tags { "RenderType"="Opaque" }
		LOD 200

		Pass
		{
			HLSLPROGRAM
			#pragma vertex vert
			#pragma fragment frag

			float4x4 unity_ObjectToWorld;
			float4x4 unity_MatrixVP;
			float4 _MainTex_ST;

			struct Vertex_Stage_Input
			{
				float4 pos : POSITION;
				float2 uv : TEXCOORD0;
			};

			struct Vertex_Stage_Output
			{
				float2 uv : TEXCOORD0;
				float4 pos : SV_POSITION;
			};

			Vertex_Stage_Output vert(Vertex_Stage_Input input)
			{
				Vertex_Stage_Output output;
				output.uv = (input.uv.xy * _MainTex_ST.xy) + _MainTex_ST.zw;
				output.pos = mul(unity_MatrixVP, mul(unity_ObjectToWorld, input.pos));
				return output;
			}

			Texture2D<float4> _MainTex;
			SamplerState sampler_MainTex;

			struct Fragment_Stage_Input
			{
				float2 uv : TEXCOORD0;
			};

			float4 frag(Fragment_Stage_Input input) : SV_TARGET
			{
				return _MainTex.Sample(sampler_MainTex, input.uv.xy);
			}

			ENDHLSL
		}
	}
	Fallback "Hidden/InternalErrorShader"
	//CustomEditor "UnityEditor.ShaderGraph.PBRMasterGUI"
}