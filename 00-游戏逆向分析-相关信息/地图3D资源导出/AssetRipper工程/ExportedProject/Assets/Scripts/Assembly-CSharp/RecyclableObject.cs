using System;
using System.Runtime.CompilerServices;
using UnityEngine;

public class RecyclableObject : MonoBehaviour
{
	public bool disabledAfterLife;

	public ObjectPool pool;

	public float lifeTime;

	[SerializeField]
	private bool roundEndRecycle;

	[CompilerGenerated]
	private Action m_WorkEvent_Listener;

	[CompilerGenerated]
	private Action m_RecycleEvent_Listener;

	[CompilerGenerated]
	private Action m_NoRoundRecycleEvent_Listener;

	public float activeTime { get; private set; }

	public bool isRecycled { get; protected set; }

	public event Action WorkEvent_Listener
	{
		[CompilerGenerated]
		add
		{
		}
		[CompilerGenerated]
		remove
		{
		}
	}

	public event Action RecycleEvent_Listener
	{
		[CompilerGenerated]
		add
		{
		}
		[CompilerGenerated]
		remove
		{
		}
	}

	public event Action NoRoundRecycleEvent_Listener
	{
		[CompilerGenerated]
		add
		{
		}
		[CompilerGenerated]
		remove
		{
		}
	}

	protected virtual void OnEnable()
	{
	}

	public void TryRecycle()
	{
	}

	public virtual void TryRecycle(bool roundRecycle)
	{
	}

	public virtual void Recycle(bool roundRecycle)
	{
	}

	protected void StartLifeTimer(float time)
	{
	}

	protected virtual void OnLifeTimerEnd()
	{
	}

	public void Active()
	{
	}

	protected virtual void Work()
	{
	}
}
