using UnityEngine;

public class SimpleHudBase : MonoBehaviour
{
	private GameObject all;

	protected virtual void Awake()
	{
	}

	protected virtual void MyPlayerInit(Player myPlayer)
	{
	}

	public virtual void SetVisible(bool value)
	{
	}
}
