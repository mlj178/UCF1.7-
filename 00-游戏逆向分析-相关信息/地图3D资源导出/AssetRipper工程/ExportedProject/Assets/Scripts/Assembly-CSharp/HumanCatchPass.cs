using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class HumanCatchPass : ScriptableRenderPass
{
	private Material mat;

	private RenderStateBlock m_RenderStateBlock;

	private FilteringSettings m_FilteringSettings;

	public HumanCatchPass(Material mat, LayerMask layerMask)
	{
	}

	public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
	{
	}
}
