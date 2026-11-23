using UnityEngine;

public class CustomTexSheet : RO_WorkListener
{
	private Material mat;

	[SerializeField]
	private Texture2D[] textures;

	[SerializeField]
	private float duration;

	[SerializeField]
	private int cycle;

	private float lifeOfCycle;

	[SerializeField]
	private float delay;

	[SerializeField]
	private float lifeTime;

	[SerializeField]
	private Gradient colorOverLife;

	private float startTime;

	private bool isContinuous;

	protected override void Awake()
	{
	}

	private void Update()
	{
	}

	private void UpdateMaterial(float lifeRate)
	{
	}

	protected override void Work()
	{
	}

	private void PlayOnce()
	{
	}
}
