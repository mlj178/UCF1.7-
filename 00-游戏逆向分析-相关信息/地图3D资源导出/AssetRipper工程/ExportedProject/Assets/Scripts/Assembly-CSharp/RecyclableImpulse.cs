using Cinemachine;
using UnityEngine;

public class RecyclableImpulse : RecyclableObject
{
	[SerializeField]
	private CinemachineImpulseSource impulse;

	public float power
	{
		set
		{
		}
	}

	public float minRadius
	{
		set
		{
		}
	}

	public float maxRadius
	{
		set
		{
		}
	}

	public float duration
	{
		set
		{
		}
	}

	protected override void Work()
	{
	}
}
