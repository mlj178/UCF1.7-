using UnityEngine;
using UnityEngine.UI;

public class CriticalDamageText : RecyclableObject
{
	[SerializeField]
	private Text dmgText;

	public void Active(int damage)
	{
	}

	protected override void Work()
	{
	}
}
