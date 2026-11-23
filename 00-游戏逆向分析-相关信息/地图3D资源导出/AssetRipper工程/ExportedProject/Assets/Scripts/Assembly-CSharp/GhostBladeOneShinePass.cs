using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class GhostBladeOneShinePass : ScriptableRenderPass
{
	private static readonly string k_RenderTag;

	private static readonly int MainTexID;

	private static readonly int TempID;

	private static readonly int RedDurationID;

	private static readonly int WhiteDurationID;

	private static readonly int PosterizePowerID;

	private GhostBladeOneShine oneShine;

	private Material mat;

	private RenderTargetIdentifier curTarget;

	public GhostBladeOneShinePass(Shader shader)
	{
	}

	public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
	{
	}

	private void Render(CommandBuffer cmd, ref RenderingData renderingData)
	{
	}

	public void Setup(in RenderTargetIdentifier curTarget)
	{
	}
}
