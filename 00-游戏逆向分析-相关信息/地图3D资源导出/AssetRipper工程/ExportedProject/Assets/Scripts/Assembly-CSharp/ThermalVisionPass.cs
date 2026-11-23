using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class ThermalVisionPass : ScriptableRenderPass
{
	private static readonly string k_RenderTag;

	private static readonly int MainTexID;

	private static readonly int TempID;

	private static readonly int DurationID;

	private static readonly int MainColorID;

	private static readonly int NoiseScaleID;

	private static readonly int NoisePowerID;

	private ThermalVision thermalVision;

	private Material mat;

	private RenderTargetIdentifier curTarget;

	public ThermalVisionPass(Shader shader)
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
