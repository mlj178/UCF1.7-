using System;
using UnityEngine;

public class EffectObj : Model
{
	[SerializeField]
	private ParticleSystem ptcSystem;

	public Transform root;

	protected bool isWorldSpace;

	protected Vector3 bindOffset;

	protected Transform bindTransform;

	public Func<bool> preRecycleFunc;

	[SerializeField]
	private float delayRecycleTime;

	private float finalRecycleTime;

	private bool fixBug;

	protected override void Work()
	{
	}

	protected virtual void LateUpdate()
	{
	}

	public override void TryRecycle(bool roundRecycle)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	public void BindOnTransformInLocalSpace(Transform bind, Vector3 offset)
	{
	}

	public void BindOnTransformInWorldSpace(Transform bind, Vector3 offset)
	{
	}

	private void BindTransform(Transform bind, Vector3 offset)
	{
	}

	protected virtual void UpdatePosition()
	{
	}

	private void StopShootEffect(bool clear)
	{
	}
}
