using System;
using System.Runtime.CompilerServices;

public class Buff
{
	public class Priority
	{
		public const int Common = 0;

		public const int Team = 1;

		public const int Life = 2;

		public const int Cheat = 999;
	}

	[CompilerGenerated]
	private Action m_timeOutAction;

	[CompilerGenerated]
	private Action m_removeAction;

	[CompilerGenerated]
	private Action m_lifeEndAction;

	public int priority;

	public string name { get; protected set; }

	public Entity owner { get; private set; }

	public float endTime { get; protected set; }

	public bool isEffective => false;

	public event Action timeOutAction
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

	public event Action removeAction
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

	public event Action lifeEndAction
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

	public Buff(string name, float duration, Entity owner)
	{
	}

	public void Refreshime(float duration)
	{
	}

	public void TimeOut()
	{
	}

	public void Remove()
	{
	}

	protected virtual void OnLifeEnd()
	{
	}
}
