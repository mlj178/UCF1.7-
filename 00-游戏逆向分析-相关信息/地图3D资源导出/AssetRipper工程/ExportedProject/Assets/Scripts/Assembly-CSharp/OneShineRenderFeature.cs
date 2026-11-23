using UnityEngine;
using UnityEngine.Rendering.Universal;

public class OneShineRenderFeature : ScriptableRendererFeature
{
	public Shader shader;

	public RenderPassEvent passEvent;

	private GhostBladeOneShinePass oneShinePass;

	public override void Create()
	{
	}

	public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
	{
	}
}
