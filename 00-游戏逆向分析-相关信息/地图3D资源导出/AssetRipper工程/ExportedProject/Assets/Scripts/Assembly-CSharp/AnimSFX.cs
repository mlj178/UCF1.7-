using UnityEngine;
using UnityEngine.UI;

public class AnimSFX : RecyclableObject
{
	[SerializeField]
	protected RawImage img;

	[SerializeField]
	protected float animTime;

	private bool isTargetFull;

	public override void Recycle(bool roundRecycle)
	{
	}

	protected override void Work()
	{
	}

	private void Animation()
	{
	}
}
