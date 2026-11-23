using System;
using UnityEngine;

[Serializable]
public struct DamageBodyRatio
{
	[SerializeField]
	private float brainRatio;

	[SerializeField]
	private float headRatio;

	[SerializeField]
	private float neckRatio;

	[SerializeField]
	private float chestRatio;

	[SerializeField]
	private float abdomenRatio;

	[SerializeField]
	private float armRatio;

	[SerializeField]
	private float handRatio;

	[SerializeField]
	private float legRatio;

	[SerializeField]
	private float footRatio;

	public float Get(string tag, float damage)
	{
		return 0f;
	}
}
