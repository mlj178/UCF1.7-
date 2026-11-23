using UnityEngine;

public class HUD_RadarIcon_Entity : HUD_RadarIcon
{
	private Entity entity;

	[SerializeField]
	private Sprite teammate;

	[SerializeField]
	private Sprite teammate_Far;

	[SerializeField]
	private Sprite teammate_Top;

	[SerializeField]
	private Sprite teammate_Bottom;

	[SerializeField]
	private Sprite teammate_Dead;

	[SerializeField]
	private Sprite enemy;

	[SerializeField]
	private Sprite enemy_Far;

	[SerializeField]
	private Sprite enemy_Top;

	[SerializeField]
	private Sprite enemy_Bottom;

	private static readonly Vector2 normalPivot;

	private static readonly Vector2 farPivot;

	protected override void Update()
	{
	}

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
