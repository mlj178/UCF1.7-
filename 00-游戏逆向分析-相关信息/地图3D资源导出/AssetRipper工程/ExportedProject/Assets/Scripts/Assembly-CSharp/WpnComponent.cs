using UnityEngine;

public class WpnComponent : MonoBehaviour
{
	protected Weapon wpn;

	protected Player owner => null;

	public virtual void Init(Weapon wpn)
	{
	}
}
