using UnityEngine;

public class HUD_RadarIcon_HearBeat : HUD_RadarIcon
{
	[SerializeField]
	private CommonHud_1 hud;

	private Entity entity;

	public override bool IsVisible()
	{
		return false;
	}

	public void Bind(Entity entity, float time)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}

	protected override void Work()
	{
	}
}
