using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class GhostBladeOneShine : VolumeComponent, IPostProcessComponent
{
	public FloatParameter RedDuration;

	public FloatParameter WhiteDuration;

	public FloatParameter PosterizePower;

	public bool IsActive()
	{
		return false;
	}

	public bool IsTileCompatible()
	{
		return false;
	}
}
