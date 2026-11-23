using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class ThermalVision : VolumeComponent, IPostProcessComponent
{
	public FloatParameter Duration;

	public ColorParameter MainColor;

	public FloatParameter NoiseScale;

	public FloatParameter NoisePower;

	public bool IsActive()
	{
		return false;
	}

	public bool IsTileCompatible()
	{
		return false;
	}
}
