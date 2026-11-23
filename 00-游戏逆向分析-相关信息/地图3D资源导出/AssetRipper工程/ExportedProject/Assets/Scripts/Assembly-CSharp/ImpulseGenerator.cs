using System.Collections;
using UnityEngine;

public class ImpulseGenerator : RO_WorkListener
{
	[SerializeField]
	private float power;

	[SerializeField]
	private float duration;

	[SerializeField]
	private float minRadius;

	[SerializeField]
	private float maxRadius;

	[SerializeField]
	private float delay;

	[SerializeField]
	private int totalCount;

	[SerializeField]
	private float interval;

	private int restCount;

	protected override void Work()
	{
	}

	private IEnumerator Generator()
	{
		return null;
	}
}
