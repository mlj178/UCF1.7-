using UnityEngine;
using UnityEngine.Rendering.Universal;

public class HumanCatchFeature : ScriptableRendererFeature
{
	public Material overrideMat;

	public LayerMask layerMask;

	public RenderPassEvent passEvent;

	private HumanCatchPass humanCatchPass;

	public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
	{
	}

	public override void Create()
	{
	}
}
