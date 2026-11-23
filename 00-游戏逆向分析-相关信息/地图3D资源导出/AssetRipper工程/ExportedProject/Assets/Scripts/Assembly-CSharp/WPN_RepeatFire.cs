using System.Collections;
using UnityEngine;
using WeaponNS.Component;

public class WPN_RepeatFire : WpnComponent
{
	private RepeatFireData data;

	private bool isOpen;

	private float nextAvailableTime;

	private Coroutine coroutine;

	private WPN_Gun gun => null;

	public override void Init(Weapon wpn)
	{
	}

	private void Update()
	{
	}

	private void AmmoBGSetting()
	{
	}

	private bool FireDisabledCheck()
	{
		return false;
	}

	private IEnumerator RepeatFireCoroutine()
	{
		return null;
	}
}
