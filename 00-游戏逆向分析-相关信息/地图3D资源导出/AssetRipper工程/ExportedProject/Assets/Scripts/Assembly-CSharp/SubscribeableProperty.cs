using System;
using System.Runtime.CompilerServices;

public class SubscribeableProperty<T1>
{
	[CompilerGenerated]
	private Action<T1, T1> m_listener;

	public T1 value { get; private set; }

	public event Action<T1, T1> listener
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

	public void Set(T1 newValue)
	{
	}
}
