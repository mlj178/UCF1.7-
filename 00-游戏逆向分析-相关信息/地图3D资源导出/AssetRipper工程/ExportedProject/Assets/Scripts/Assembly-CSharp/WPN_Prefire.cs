using UnityEngine;

public class WPN_Prefire : WpnComponent
{
	[SerializeField]
	private float penalty;

	private float prefireAnimTime;

	private float needDelayTime;

	private WPN_Gun gun;

	public override void Init(Weapon wpn)
	{
	}

	private void OnEnable()
	{
	}

	private void Update()
	{
	}

	private void GetPrefireAnimTime()
	{
	}

	private bool Prefire()
	{
		return false;
	}
}
