public class HUD_RadarIcon_Alive : HUD_RadarIcon
{
	private Entity entity;

	public override bool IsVisible()
	{
		return false;
	}

	public void Bind(Entity entity)
	{
	}

	public override void Recycle(bool roundRecycle)
	{
	}
}
