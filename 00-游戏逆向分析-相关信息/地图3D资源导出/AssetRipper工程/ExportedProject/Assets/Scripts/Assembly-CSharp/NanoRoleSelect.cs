using System;
using System.Runtime.CompilerServices;

public class NanoRoleSelect
{
	public enum Type
	{
		None = 0,
		Normal = 1,
		Hero = 2,
		Terminataor = 3
	}

	private Player owner;

	private int selection;

	private bool closeWhenDead;

	[CompilerGenerated]
	private Action<Type> m_Type_Listnner;

	public Type tableType { get; private set; }

	public float closeTime { get; private set; }

	public bool isClosed => false;

	public event Action<Type> Type_Listnner
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

	public NanoRoleSelect(Player player)
	{
	}

	public void TryOpenNormal()
	{
	}

	public void OpenMasterRole(bool isHero)
	{
	}

	private void SetType(Type newType)
	{
	}

	public void Open(Type type, float time)
	{
	}

	public void Close()
	{
	}

	public void Select(int key)
	{
	}

	private void OnLifeStateChange(bool isAlive)
	{
	}

	private void Active()
	{
	}

	private void SelectNanoGhost()
	{
	}

	private void SelectHero()
	{
	}

	private void SelectTerminator()
	{
	}

	public void Update()
	{
	}
}
