using UnityEngine;

public class HUD_SupplyBoxSign : HUD_ProjectionSign
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

	protected override bool GetVisible()
	{
		return false;
	}

	public void Bind(SupplyBox supplyBox)
	{
	}
}
