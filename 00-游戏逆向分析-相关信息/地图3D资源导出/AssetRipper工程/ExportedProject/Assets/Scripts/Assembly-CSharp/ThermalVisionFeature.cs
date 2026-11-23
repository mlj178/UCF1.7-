using UnityEngine;
using UnityEngine.Rendering.Universal;

public class ThermalVisionFeature : ScriptableRendererFeature
{
	public Shader shader;

	public RenderPassEvent passEvent;

	private ThermalVisionPass thermalVisionPass;

	public override void Create()
	{
	}

	public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
	{
	}
}
