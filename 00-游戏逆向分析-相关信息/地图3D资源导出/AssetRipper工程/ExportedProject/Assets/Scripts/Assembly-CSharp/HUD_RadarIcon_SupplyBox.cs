using UnityEngine;

public class HUD_RadarIcon_SupplyBox : HUD_RadarIcon
{
	private SupplyBox.Type supplyBoxType;

	[SerializeField]
	private Sprite yellow;

	[SerializeField]
	private Sprite red;

	[SerializeField]
	private Sprite blue;

	protected override void Update()
	{
	}

	public override bool IsVisible()
	{
		return false;
	}

	public void Bind(SupplyBox supplyBox)
	{
	}
}
